from unittest.mock import call

import pytest

from toga.colors import rgb
from toga.fonts import SYSTEM_DEFAULT_FONT_SIZE, Font
from toga.style.pack import (
    BOLD,
    CENTER,
    COLUMN,
    HIDDEN,
    ITALIC,
    LEFT,
    NONE,
    RIGHT,
    RTL,
    SMALL_CAPS,
    SYSTEM,
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


@pytest.mark.parametrize(
    "kwargs",
    [
        # Test with both shorthand and with individual properties.
        {"font": ("normal", "small-caps", "bold", 12, "Roboto")},
        {
            "font_family": "Roboto",
            "font_size": 12,
            "font_style": "normal",
            "font_variant": "small-caps",
            "font_weight": "bold",
        },
    ],
)
def test_set_font(kwargs):
    style = Pack(**kwargs)
    root = ExampleNode("app", style=style)
    root.style.apply()
    # Should only be called once, despite multiple font-related properties being set.
    root._impl.set_font.assert_called_once_with(
        Font("Roboto", 12, style="normal", variant="small-caps", weight="bold")
    )
    root.refresh.assert_called_once_with()


@pytest.mark.parametrize(
    "family, result",
    [
        ("Courier", "Courier"),
        (["Courier", "Helvetica"], "Courier"),
        (["Bogus Font", "Courier", "Helvetica"], "Courier"),
        (["Courier", "Bogus Font", "Helvetica"], "Courier"),
        (["Bogus Font"], SYSTEM),
        ("Bogus Font", SYSTEM),
    ],
)
def test_set_font_family(family, result):
    """The first viable family is used. Dummy backend rejects 'Bogus Font'."""
    node = ExampleNode("app", style=Pack(font_family=family))
    node.style.apply()
    node._impl.set_font.assert_called_once_with(Font(result, SYSTEM_DEFAULT_FONT_SIZE))


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


def test_set_visibility_hidden():
    root = ExampleNode("app", style=Pack(visibility=HIDDEN))
    root.style.apply()
    root._impl.set_hidden.assert_called_once_with(True)


def test_set_visibility_inherited():
    """Nodes should be hidden when an ancestor is hidden."""
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
    grandparent.style.visibility = HIDDEN
    assert_hidden_called(True, True, True)

    # Just setting child or parent to VISIBLE won't trigger an apply, because that's
    # their default value. So first, set them to hidden.
    parent.style.visibility = HIDDEN
    assert_hidden_called(None, True, True)

    child.style.visibility = HIDDEN
    assert_hidden_called(None, None, True)

    # Then set them to visible. They should still not actually be shown.
    parent.style.visibility = VISIBLE
    assert_hidden_called(None, True, True)

    child.style.visibility = VISIBLE
    assert_hidden_called(None, None, True)

    # Show grandparent again; the other two should reappear.
    grandparent.style.visibility = VISIBLE
    assert_hidden_called(False, False, False)
