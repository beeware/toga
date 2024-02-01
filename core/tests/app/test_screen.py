from PIL.Image import Image as PILImage

from toga.images import Image as TogaImage
from toga_dummy.utils import assert_action_performed


def test_name(app):
    """The name of the screens can be retrieved"""
    assert app.screens[0].name == "Primary Screen"
    assert app.screens[1].name == "Secondary Screen"


def test_origin(app):
    """The origin of the screens can be retrieved"""
    assert app.screens[0].origin == (0, 0)
    assert app.screens[1].origin == (-1366, -768)


def test_size(app):
    """The size of the screens can be retrieved"""
    assert app.screens[0].size == (1920, 1080)
    assert app.screens[1].size == (1366, 768)


def test_as_image(app):
    """A screen can be captured as an image"""
    for screen in app.screens:
        # `as_image()` should default to `toga.images.Image` as format.
        toga_image_screenshot = screen.as_image()
        assert_action_performed(screen, "get image data")
        # Check if returned image is of type `toga.images.Image`.
        assert isinstance(toga_image_screenshot, TogaImage)
        # Don't need to check the raw data; just check it's the right screen size.
        assert toga_image_screenshot.size == screen.size

        pil_screenshot = screen.as_image(format=PILImage)
        assert_action_performed(screen, "get image data")
        # Check if returned image is of type `PIL.Image.Image`.
        assert isinstance(pil_screenshot, PILImage)
        assert pil_screenshot.size == screen.size
