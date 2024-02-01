from importlib import import_module

import pytest
from PIL.Image import Image as PILImage

from toga.images import Image as TogaImage


@pytest.fixture
def screen_probe_list(app):
    module = import_module("tests_backend.screen")
    return [getattr(module, "ScreenProbe")(app, screen) for screen in app.screens]


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
    # Using a probe for test as the feature is not implemented on some platforms.
    for screen_probe in screen_probe_list:
        # `get_screenshot()` should default to `toga.images.Image` as format.
        toga_image_screenshot = screen_probe.get_screenshot()
        # Check if returned image is of type `toga.images.Image`.
        assert isinstance(toga_image_screenshot, TogaImage)
        assert toga_image_screenshot.size == screen_probe.screen.size

        pil_screenshot = screen_probe.get_screenshot(format=PILImage)
        # Check if returned image is of type `PIL.Image.Image`.
        assert isinstance(pil_screenshot, PILImage)
        assert pil_screenshot.size == screen_probe.screen.size
