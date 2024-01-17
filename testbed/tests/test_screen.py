from importlib import import_module

import pytest

from toga.screen import Screen as ScreenInterface


@pytest.fixture
def screen_probe_list(app):
    module = import_module("tests_backend.screen")
    return [getattr(module, "ScreenProbe")(screen) for screen in app.screens]


async def test_type(screen_probe_list):
    for screen_probe in screen_probe_list:
        assert isinstance(screen_probe.screen, ScreenInterface)
        screen_probe.assert_implementation_type()
        screen_probe.assert_native_type()


async def test_name(screen_probe_list):
    for screen_probe in screen_probe_list:
        assert isinstance(screen_probe.screen.name, str)
        screen_probe.assert_name()


async def test_origin(screen_probe_list):
    for screen_probe in screen_probe_list:
        origin = screen_probe.screen.origin
        assert (
            isinstance(origin, tuple)
            and len(origin) == 2
            and all(isinstance(val, int) for val in origin)
        )
        screen_probe.assert_origin()


async def test_size(screen_probe_list):
    for screen_probe in screen_probe_list:
        size = screen_probe.screen.size
        assert (
            isinstance(size, tuple)
            and len(size) == 2
            and all(isinstance(val, int) for val in size)
        )
        screen_probe.assert_size()


async def test_as_image(screen_probe_list):
    for screen_probe in screen_probe_list:
        screen_probe.assert_screen_as_image_size()
