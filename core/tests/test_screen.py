from toga_dummy.utils import assert_action_performed


def test_name(app):
    assert app.screens[0].name == "primary_screen"
    assert app.screens[1].name == "secondary_screen"


def test_origin(app):
    assert app.screens[0].origin == (0, 0)
    assert app.screens[1].origin == (-1920, 0)


def test_size(app):
    assert app.screens[0].size == (1920, 1080)
    assert app.screens[1].size == (1920, 1080)


# Same as for the window as_image() test.
def test_as_image(app):
    """A screen can be captured as an image"""
    image = app.screens[0].as_image()
    assert_action_performed(app.screens[0], "get image data")
    # Don't need to check the raw data; just check it's the right size.
    assert image.size == (318, 346)
