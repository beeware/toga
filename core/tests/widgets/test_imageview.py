from pytest import fail, fixture

import toga
from toga_dummy.utils import assert_action_performed


@fixture
def widget():
    return toga.ImageView()


def test_widget_created(widget):
    assert widget._impl.interface is widget
    assert_action_performed(widget, "create ImageView")


def test_setting_image_invokes_impl_method(widget):
    new_image = "not a image"

    # Binding a non-existent image raises an exception
    try:
        widget.image = new_image
        fail("Image should not bind")
    except FileNotFoundError:
        pass

    # self.assertEqual(widget._image, new_image)
    # self.assertValueSet(widget, 'image', new_image)
