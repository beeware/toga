import os
from importlib import import_module

import pytest

from toga.platform import current_platform
from toga.screen import Screen as ScreenInterface


@pytest.fixture
def screen_probe_list(app):
    module = import_module("tests_backend.screen")
    if current_platform == "android":
        return [getattr(module, "ScreenProbe")(app, screen) for screen in app.screens]
    else:
        return [getattr(module, "ScreenProbe")(screen) for screen in app.screens]


async def test_type(screen_probe_list):
    """The type of the implementation and native classes should be correct"""
    for screen_probe in screen_probe_list:
        assert isinstance(screen_probe.screen, ScreenInterface)
        screen_probe.assert_implementation_type()
        screen_probe.assert_native_type()


async def test_name(screen_probe_list):
    """The name of the screens can be retrieved"""
    for screen_probe in screen_probe_list:
        assert isinstance(screen_probe.screen.name, str)
        screen_probe.assert_name()


async def test_origin(screen_probe_list):
    """The origin of the screens can be retrieved"""
    for screen_probe in screen_probe_list:
        origin = screen_probe.screen.origin
        assert (
            isinstance(origin, tuple)
            and len(origin) == 2
            and all(isinstance(val, int) for val in origin)
        )
        screen_probe.assert_origin()


async def test_size(screen_probe_list):
    """The size of the screens can be retrieved"""
    for screen_probe in screen_probe_list:
        size = screen_probe.screen.size
        assert (
            isinstance(size, tuple)
            and len(size) == 2
            and all(isinstance(val, int) for val in size)
        )
        screen_probe.assert_size()


async def test_as_image(screen_probe_list):
    """A screen can be captured as an image"""
    for screen_probe in screen_probe_list:
        if current_platform in {"android", "iOS", "textual"}:
            pytest.xfail("Screen.as_image is not implemented on current platform.")
        elif (
            current_platform == "linux"
            and os.environ.get("XDG_SESSION_TYPE", "").lower() != "x11"
        ):
            pytest.xfail("Screen.as_image() is not supported on wayland.")
        screenshot = screen_probe.screen.as_image()
        assert screenshot.size == screen_probe.screen.size
