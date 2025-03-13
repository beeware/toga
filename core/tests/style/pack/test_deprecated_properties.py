import pytest

from toga.style.pack import (
    BOTTOM,
    CENTER,
    COLUMN,
    END,
    LEFT,
    LTR,
    RIGHT,
    ROW,
    RTL,
    START,
    TOP,
    Pack,
)

from . import (
    assert_name_in,
    assert_name_not_in,
    delitem,
    delitem_hyphen,
    getitem,
    getitem_hyphen,
    with_init,
    with_setattr,
    with_setitem,
    with_setitem_hyphen,
    with_update,
)


@pytest.mark.parametrize(
    "old_name, new_name, value, default",
    [
        ("padding", "margin", (5, 5, 5, 5), (0, 0, 0, 0)),
        ("padding_top", "margin_top", 5, 0),
        ("padding_right", "margin_right", 5, 0),
        ("padding_bottom", "margin_bottom", 5, 0),
        ("padding_left", "margin_left", 5, 0),
    ],
)
@pytest.mark.parametrize(
    "style_with",
    (with_init, with_update, with_setattr, with_setitem, with_setitem_hyphen),
)
@pytest.mark.parametrize("get_fn", (getattr, getitem, getitem_hyphen))
@pytest.mark.parametrize("del_fn", (delattr, delitem, delitem_hyphen))
def test_padding_margin(old_name, new_name, value, default, style_with, get_fn, del_fn):
    """Padding (with deprecation warning) and margin map to each other."""
    # Set the old name, then check the new name
    with pytest.warns(DeprecationWarning):
        style = style_with(**{old_name: value})
    assert_name_in(new_name, style)
    assert get_fn(style, new_name) == value

    # Delete the old name, check new name
    with pytest.warns(DeprecationWarning):
        del_fn(style, old_name)
    assert_name_not_in(new_name, style)
    assert get_fn(style, new_name) == default

    # Set the new name, then check the old name
    style = style_with(**{new_name: value})
    with pytest.warns(DeprecationWarning):
        assert_name_in(old_name, style)
    with pytest.warns(DeprecationWarning):
        assert get_fn(style, old_name) == value

    # Delete the new name, check old name
    del_fn(style, new_name)
    with pytest.warns(DeprecationWarning):
        assert_name_not_in(old_name, style)
    with pytest.warns(DeprecationWarning):
        assert get_fn(style, old_name) == default


@pytest.mark.parametrize(
    "direction, text_direction, alignment, align_items",
    [
        (ROW, LTR, TOP, START),
        (ROW, RTL, TOP, START),
        (ROW, LTR, BOTTOM, END),
        (ROW, RTL, BOTTOM, END),
        (ROW, LTR, CENTER, CENTER),
        (ROW, RTL, CENTER, CENTER),
        (COLUMN, LTR, LEFT, START),
        (COLUMN, RTL, LEFT, END),
        (COLUMN, LTR, RIGHT, END),
        (COLUMN, RTL, RIGHT, START),
        (COLUMN, RTL, CENTER, CENTER),
        (COLUMN, LTR, CENTER, CENTER),
    ],
)
@pytest.mark.parametrize(
    "style_with",
    (with_init, with_update, with_setattr, with_setitem, with_setitem_hyphen),
)
@pytest.mark.parametrize("get_fn", (getattr, getitem, getitem_hyphen))
@pytest.mark.parametrize("del_fn", (delattr, delitem, delitem_hyphen))
def test_alignment_align_items(
    direction, text_direction, alignment, align_items, style_with, get_fn, del_fn
):
    """Alignment (with deprecation warning) and align_items map to each other."""
    # Set alignment, check align_items
    with pytest.warns(DeprecationWarning):
        style = style_with(alignment=alignment)
        style.update(direction=direction, text_direction=text_direction)

    assert get_fn(style, "align_items") == align_items

    # Delete alignment, check align_items
    with pytest.warns(DeprecationWarning):
        del_fn(style, "alignment")
    assert get_fn(style, "align_items") is None

    # Set align_items, check alignment
    style = style_with(align_items=align_items)
    style.update(direction=direction, text_direction=text_direction)

    with pytest.warns(DeprecationWarning):
        assert get_fn(style, "alignment") == alignment

    # Delete align_items, check alignment
    del_fn(style, "align_items")
    with pytest.warns(DeprecationWarning):
        assert get_fn(style, "alignment") is None


@pytest.mark.parametrize(
    "direction, alignment",
    [
        (ROW, LEFT),
        (ROW, RIGHT),
        (COLUMN, TOP),
        (COLUMN, BOTTOM),
    ],
)
@pytest.mark.parametrize("get_fn", (getattr, getitem, getitem_hyphen))
def test_alignment_align_items_invalid(direction, alignment, get_fn):
    """Invalid settings for alignment should return None for align_items."""
    with pytest.warns(DeprecationWarning):
        style = Pack(direction=direction, alignment=alignment)
    assert get_fn(style, "align_items") is None


def test_bogus_property_name():
    """Invalid property name in brackets should be an error.

    This is tested here along with deprecated property names, because normally it should
    be verified by Travertino's tests. It can only be an issue as long as we're
    overriding the relevant methods in Pack.
    """
    style = Pack()

    with pytest.raises(KeyError):
        style["bogus"] = 1
    with pytest.raises(KeyError):
        style["bogus"]
    with pytest.raises(KeyError):
        del style["bogus"]
