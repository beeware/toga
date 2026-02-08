from importlib import import_module

from PIL.Image import Image as PILImage

from toga.images import Image as TogaImage


def screen_probe(screen):
    module = import_module("tests_backend.screens")
    return module.ScreenProbe(screen)


async def test_name(app):
    """The name of the screens can be retrieved"""
    for screen in app.screens:
        # Just check that it returns a string as the name will be platform specific.
        assert isinstance(screen.name, str)


async def test_origin(app):
    """The origin of the screens can be retrieved"""
    for screen in app.screens:
        origin = screen.origin
        assert isinstance(origin, tuple)
        assert len(origin) == 2
        assert all(isinstance(val, int) for val in origin)


async def test_size(app):
    """The size of the screens can be retrieved"""
    for screen in app.screens:
        size = screen.size
        assert isinstance(size, tuple)
        assert len(size) == 2
        # Check that neither the width or height is zero.
        assert all(isinstance(val, int) and val > 0 for val in size)


async def test_as_image(app):
    """A screen can be captured as an image"""
    # Using a probe for test as the feature is not implemented on some platforms.
    for screen in app.screens:
        probe = screen_probe(screen)

        # `get_screenshot()` should default to `toga.images.Image` as format.
        screenshot = probe.get_screenshot()
        await probe.redraw(f"Screenshot of {screen} has been taken")
        # Check if returned image is of type `toga.images.Image`.
        assert isinstance(screenshot, TogaImage)
        probe.assert_image_size(
            screenshot.size,
            probe.screen.size,
            screen=probe.screen,
        )

        # Capture screenshot in PIL format
        pil_screenshot = probe.get_screenshot(format=PILImage)
        await probe.redraw(f"Screenshot of {screen} has been taken in PIL format")
        # Check if returned image is of type `PIL.Image.Image`.
        assert isinstance(pil_screenshot, PILImage)
        probe.assert_image_size(
            pil_screenshot.size,
            probe.screen.size,
            screen=probe.screen,
        )
