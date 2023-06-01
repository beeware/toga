from pathlib import Path
from unittest.mock import ANY

import pytest

import toga
from toga_dummy.paths import Paths
from toga_dummy.utils import assert_action_performed, assert_action_performed_with


@pytest.fixture
def app(monkeypatch):
    # Monkeypatch a known app path into the paths module.
    monkeypatch.setattr(Paths, "app", Path(toga.__file__).parent)


@pytest.fixture
def widget():
    return toga.ImageView()


def test_widget_created(widget):
    "A empty ImageView can be created"

    # interface/impl round trips
    assert widget._impl.interface is widget
    assert_action_performed(widget, "create ImageView")
    assert_action_performed_with(widget, "set image", image=None)
    assert_action_performed(widget, "refresh")

    assert widget.image is None


def test_widget_created_with_args(app, widget):
    "An ImageView can be created with argumentgs"
    image = toga.Image(Path("resources") / "toga.png")
    widget = toga.ImageView(image=image)

    # interface/impl round trips
    assert widget._impl.interface is widget
    assert_action_performed(widget, "create ImageView")
    assert_action_performed_with(widget, "set image", image=image)
    assert_action_performed(widget, "refresh")

    # Image attribute is set
    assert widget.image == image


def test_set_image_str(app, widget):
    "The image can be set with a string"
    widget.image = "https://example.com/image.jpg"
    assert_action_performed_with(widget, "set image", image=ANY)
    assert_action_performed(widget, "refresh")

    assert isinstance(widget.image, toga.Image)
    assert widget.image.path == "https://example.com/image.jpg"


def test_set_image_path(app, widget):
    "The image can be set with a Path"
    widget.image = Path("resources") / "toga.png"
    assert_action_performed_with(widget, "set image", image=ANY)
    assert_action_performed(widget, "refresh")

    assert isinstance(widget.image, toga.Image)
    assert widget.image.path == Path(toga.__file__).parent / "resources" / "toga.png"


def test_set_image(app, widget):
    "The image can be set with an Image instance"
    image = toga.Image(Path("resources") / "toga.png")

    widget.image = image
    assert_action_performed_with(widget, "set image", image=image)
    assert_action_performed(widget, "refresh")

    assert widget.image == image


def test_set_image_none(app):
    "The image can be cleared"
    widget = toga.ImageView(image="https://example.com/image.jpg")
    assert widget.image is not None

    widget.image = None
    assert_action_performed_with(widget, "set image", image=None)
    assert_action_performed(widget, "refresh")

    assert widget.image is None
