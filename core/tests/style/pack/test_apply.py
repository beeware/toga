from unittest.mock import call

from toga.colors import rgb
from toga.fonts import Font
from toga.style.pack import (
    CENTER,
    HIDDEN,
    LEFT,
    RIGHT,
    RTL,
    Pack,
)

from .utils import ExampleNode


def test_set_default_right_textalign_when_rtl():
    root = ExampleNode("app", style=Pack(text_direction=RTL))
    root.style.reapply()
    # Two calls; one caused by text_align, one because text_direction
    # implies a change to text alignment.
    assert root._impl.set_alignment.mock_calls == [call(RIGHT), call(RIGHT)]


def test_set_default_left_textalign_when_no_rtl():
    root = ExampleNode("app", style=Pack())
    root.style.reapply()
    # Two calls; one caused by text_align, one because text_direction
    # implies a change to text alignment.
    assert root._impl.set_alignment.mock_calls == [call(LEFT), call(LEFT)]


def test_set_center_alignment():
    root = ExampleNode("app", style=Pack(text_align="center"))
    root.style.reapply()
    root._impl.set_alignment.assert_called_once_with(CENTER)


def test_set_color():
    color = "#ffffff"
    root = ExampleNode("app", style=Pack(color=color))
    root.style.reapply()
    root._impl.set_color.assert_called_once_with(rgb(255, 255, 255))


def test_set_background_color():
    color = "#ffffff"
    root = ExampleNode("app", style=Pack(background_color=color))
    root.style.reapply()
    root._impl.set_background_color.assert_called_once_with(rgb(255, 255, 255))


def test_set_font():
    root = ExampleNode(
        "app",
        style=Pack(
            font_family="Roboto",
            font_size=12,
            font_style="normal",
            font_variant="small-caps",
            font_weight="bold",
        ),
    )
    root.style.reapply()
    root._impl.set_font.assert_called_with(
        Font("Roboto", 12, style="normal", variant="small-caps", weight="bold")
    )
    root.refresh.assert_called_with()


def test_set_visibility_hidden():
    root = ExampleNode("app", style=Pack(visibility=HIDDEN))
    root.style.reapply()
    root._impl.set_hidden.assert_called_once_with(True)
