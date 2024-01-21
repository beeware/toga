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
    screenshot = app.screens[0].as_image()
    assert_action_performed(app.screens[0], "get image data")
    # Don't need to check the raw data; just check it's the right screen size.
    assert screenshot.size == app.screens[0].size
