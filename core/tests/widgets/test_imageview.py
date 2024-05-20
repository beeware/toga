from pathlib import Path
from unittest.mock import ANY

import PIL.Image
import pytest
from travertino.size import at_least

import toga
from toga.style.pack import Pack
from toga.widgets.imageview import rehint_imageview
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


@pytest.fixture
def widget(app):
    return toga.ImageView()


def test_create_empty(widget):
    """An empty ImageView can be created."""
    # interface/impl round trips
    assert widget._impl.interface is widget
    assert_action_performed(widget, "create ImageView")
    assert_action_performed_with(widget, "set image", image=None)
    assert_action_performed(widget, "refresh")

    assert widget.image is None


ABSOLUTE_FILE_PATH = Path(__file__).parent.parent / "resources/toga.png"


def test_create_from_toga_image(app):
    """An ImageView can be created from a Toga image."""
    image = toga.Image(ABSOLUTE_FILE_PATH)
    widget = toga.ImageView(image=image)

    # Interface/impl round trips
    assert widget._impl.interface is widget
    assert_action_performed(widget, "create ImageView")
    assert_action_performed_with(widget, "set image", image=image)
    assert_action_performed(widget, "refresh")

    # Image attribute is set
    assert widget.image == image


def test_create_from_pil():
    """An ImageView can be created from a PIL image."""
    with PIL.Image.open(ABSOLUTE_FILE_PATH) as pil_img:
        pil_img.load()

    imageview = toga.ImageView(pil_img)
    assert isinstance(imageview.image, toga.Image)
    assert imageview.image.size == (32, 32)


def test_disable_no_op(widget):
    """ImageView doesn't have a disabled state."""

    # Enabled by default
    assert widget.enabled

    # Try to disable the widget
    widget.enabled = False

    # Still enabled.
    assert widget.enabled


def test_focus_noop(widget):
    """Focus is a no-op."""
    widget.focus()
    assert_action_not_performed(widget, "focus")


def test_set_image_str(widget):
    """The image can be set with a string."""
    widget.image = ABSOLUTE_FILE_PATH

    assert_action_performed_with(widget, "set image", image=ANY)
    assert_action_performed(widget, "refresh")

    assert isinstance(widget.image, toga.Image)
    assert widget.image.path == ABSOLUTE_FILE_PATH


def test_set_image_path(widget):
    """The image can be set with a Path."""
    widget.image = Path(ABSOLUTE_FILE_PATH)

    assert_action_performed_with(widget, "set image", image=ANY)
    assert_action_performed(widget, "refresh")

    assert isinstance(widget.image, toga.Image)
    assert widget.image.path == ABSOLUTE_FILE_PATH


def test_set_image(widget):
    """The image can be set with an Image instance."""
    image = toga.Image(Path(ABSOLUTE_FILE_PATH))
    widget.image = image
    assert_action_performed_with(widget, "set image", image=image)
    assert_action_performed(widget, "refresh")

    assert widget.image == image


def test_set_image_none(app):
    """The image can be cleared."""
    widget = toga.ImageView(image=ABSOLUTE_FILE_PATH)
    assert widget.image is not None

    widget.image = None
    assert_action_performed_with(widget, "set image", image=None)
    assert_action_performed(widget, "refresh")

    assert widget.image is None


@pytest.mark.parametrize(
    "params, expected_width, expected_height, expected_aspect_ratio",
    [
        # Intrinsic image size
        (dict(style=Pack()), 144, 72, 2),
        (dict(style=Pack(), scale=2), 288, 144, 2),
        # Fixed width
        (dict(style=Pack(width=150)), 150, 75, 2),
        (dict(style=Pack(width=150), scale=2), 300, 150, 2),
        # Fixed height
        (dict(style=Pack(height=80)), 160, 80, 2),
        (dict(style=Pack(height=80), scale=2), 320, 160, 2),
        # Explicit image size
        (dict(style=Pack(width=37, height=42)), 37, 42, None),
        (dict(style=Pack(width=37, height=42), scale=2), 74, 84, None),
        # Intrinsic image size, flex widget
        (dict(style=Pack(flex=1)), at_least(0), at_least(0), 2),
        (dict(style=Pack(flex=1), scale=2), at_least(0), at_least(0), 2),
        # Fixed width, flex widget
        (dict(style=Pack(width=150, flex=1)), 150, at_least(0), 2),
        (dict(style=Pack(width=150, flex=1), scale=2), 300, at_least(0), 2),
        # Fixed height, flex widget
        (dict(style=Pack(height=80, flex=1)), at_least(0), 80, 2),
        (dict(style=Pack(height=80, flex=1), scale=2), at_least(0), 160, 2),
        # Explicit image size, flex widget
        (dict(style=Pack(width=37, height=42, flex=1)), 37, 42, None),
        (dict(style=Pack(width=37, height=42, flex=1), scale=2), 74, 84, None),
    ],
)
def test_rehint_image(
    app,
    params,
    expected_width,
    expected_height,
    expected_aspect_ratio,
):
    path = Path(__file__).parent.parent / "resources/sample.png"
    image = toga.Image(path)

    width, height, aspect_ratio = rehint_imageview(image=image, **params)
    assert width == expected_width
    assert height == expected_height
    assert aspect_ratio == expected_aspect_ratio


@pytest.mark.parametrize(
    "params",
    [
        # Default scale
        dict(style=Pack()),
        # Explicit width/height
        dict(style=Pack(width=100)),
        dict(style=Pack(height=200)),
        dict(style=Pack(width=100, height=200)),
        # 2x Scale
        dict(style=Pack(), scale=2),
    ],
)
def test_rehint_empty_image(params):
    width, height, aspect_ratio = rehint_imageview(image=None, **params)
    assert width == 0
    assert height == 0
    assert aspect_ratio is None


def test_as_image_toga():
    toga_img = toga.Image(ABSOLUTE_FILE_PATH)
    imageview = toga.ImageView(toga_img)
    toga_img_2 = imageview.as_image()
    assert isinstance(toga_img_2, toga.Image)
    assert toga_img_2.size == (32, 32)


def test_as_image_pil():
    imageview = toga.ImageView(ABSOLUTE_FILE_PATH)
    pil_img = imageview.as_image(PIL.Image.Image)
    assert isinstance(pil_img, PIL.Image.Image)
    assert pil_img.size == (32, 32)
