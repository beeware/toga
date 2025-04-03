from unittest.mock import call

import pytest

from toga.colors import rgb
from toga.fonts import Font
from toga.style.pack import (
    BOLD,
    CENTER,
    COLUMN,
    HIDDEN,
    ITALIC,
    LEFT,
    NONE,
    PACK,
    RIGHT,
    RTL,
    SMALL_CAPS,
    VISIBLE,
    Pack,
)

from .utils import ExampleNode, ExampleParentNode


def test_set_default_right_textalign_when_rtl():
    root = ExampleNode("app", style=Pack(text_direction=RTL))
    root.style.apply()
    # Two calls; one caused by text_align, one because text_direction
    # implies a change to text alignment.
    assert root._impl.set_text_align.mock_calls == [call(RIGHT), call(RIGHT)]


def test_set_default_left_textalign_when_no_rtl():
    root = ExampleNode("app", style=Pack())
    root.style.apply()
    # Two calls; one caused by text_align, one because text_direction
    # implies a change to text alignment.
    assert root._impl.set_text_align.mock_calls == [call(LEFT), call(LEFT)]


def test_set_center_text_align():
    root = ExampleNode("app", style=Pack(text_align="center"))
    root.style.apply()
    root._impl.set_text_align.assert_called_once_with(CENTER)


def test_set_color():
    color = "#ffffff"
    root = ExampleNode("app", style=Pack(color=color))
    root.style.apply()
    root._impl.set_color.assert_called_once_with(rgb(255, 255, 255))


def test_set_background_color():
    color = "#ffffff"
    root = ExampleNode("app", style=Pack(background_color=color))
    root.style.apply()
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
    root.style.apply()
    # Should only be called once, despite multiple font-related properties being set.
    root._impl.set_font.assert_called_once_with(
        Font("Roboto", 12, style="normal", variant="small-caps", weight="bold")
    )
    root.refresh.assert_called_once_with()


def test_set_multiple_layout_properties():
    """Setting multiple layout properties at once should only trigger one refresh."""
    root = ExampleNode(
        "app",
        style=Pack(
            # All properties which can affect layout:
            display=NONE,
            direction=COLUMN,
            align_items=CENTER,
            justify_content=CENTER,
            gap=5,
            width=100,
            height=100,
            flex=5,
            margin=5,
            margin_top=5,
            margin_right=5,
            margin_bottom=5,
            margin_left=5,
            text_direction=RTL,
            font_family="A Family",
            font_style=ITALIC,
            font_variant=SMALL_CAPS,
            font_weight=BOLD,
            font_size=12,
        ),
    )
    root.style.apply()
    root.refresh.assert_called_once_with()


@pytest.mark.parametrize(
    "name, value",
    [
        ("visibility", HIDDEN),
        ("display", NONE),
    ],
)
def test_set_visibility_hidden(name, value):
    root = ExampleNode("app", style=Pack(**{name: value}))
    root.style.apply()
    root._impl.set_hidden.assert_called_once_with(True)


@pytest.mark.parametrize(
    "name, on, off",
    [
        ("visibility", VISIBLE, HIDDEN),
        ("display", PACK, NONE),
    ],
)
def test_set_visibility_inherited(name, on, off):
    """Nodes should be hidden when an ancestor is hidden via display or visibility."""
    grandparent = ExampleParentNode("grandparent", style=Pack())
    parent = ExampleParentNode("parent", style=Pack())
    child = ExampleNode("child", style=Pack())
    grandparent.add(parent)
    parent.add(child)

    def assert_hidden_called(grandparent_value, parent_value, child_value):
        for node, value in [
            (grandparent, grandparent_value),
            (parent, parent_value),
            (child, child_value),
        ]:
            if value is None:
                node._impl.set_hidden.assert_not_called()
            else:
                node._impl.set_hidden.assert_called_once_with(value)

            node._impl.set_hidden.reset_mock()

    # Hiding grandparent should hide all.
    grandparent.style[name] = off
    assert_hidden_called(True, True, True)

    # Just setting child or parent to VISIBLE won't trigger an apply, because that's
    # their default value. So first, set them to hidden.
    parent.style[name] = off
    assert_hidden_called(None, True, True)

    child.style[name] = off
    assert_hidden_called(None, None, True)

    # Then set them to visible. They should still not actually be shown.
    parent.style[name] = on
    assert_hidden_called(None, True, True)

    child.style[name] = on
    assert_hidden_called(None, None, True)

    # Show grandparent again; the other two should reappear.
    grandparent.style[name] = on
    assert_hidden_called(False, False, False)
