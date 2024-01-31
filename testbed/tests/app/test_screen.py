from importlib import import_module

import pytest

from toga.platform import current_platform


@pytest.fixture
def screen_probe_list(app):
    module = import_module("tests_backend.screen")
    if current_platform == "android":
        return [getattr(module, "ScreenProbe")(app, screen) for screen in app.screens]
    else:
        return [getattr(module, "ScreenProbe")(screen) for screen in app.screens]


async def test_name(app):
    """The name of the screens can be retrieved"""
    for screen in app.screens:
        # Just check that it returns a string as the name will be platform specific.
        assert isinstance(screen.name, str)


async def test_origin(app):
    """The origin of the screens can be retrieved"""
    for screen in app.screens:
        origin = screen.origin
        assert (
            isinstance(origin, tuple)
            and len(origin) == 2
            and all(isinstance(val, int) for val in origin)
        )


async def test_size(app):
    """The size of the screens can be retrieved"""
    for screen in app.screens:
        size = screen.size
        assert (
            isinstance(size, tuple)
            and len(size) == 2
            # Check that neither the width or height is zero.
            and all(isinstance(val, int) and val > 0 for val in size)
        )


async def test_as_image(screen_probe_list):
    """A screen can be captured as an image"""
    for screen_probe in screen_probe_list:
        # Using a probe for test as feature is not implemented on some platforms.
        screenshot = screen_probe.get_screenshot()
        assert screenshot.size == screen_probe.screen.size
