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


def setitem(obj, name, value):
    obj[name] = value


def getitem(obj, name):
    return obj[name]


def delitem(obj, name):
    del obj[name]


@pytest.mark.parametrize(
    "old_name, new_name, value, default",
    [
        # Travertino 0.3.0 doesn't support accessing a directional property via bracket
        # notation.
        # ("padding", "margin", (5, 5, 5, 5), (0, 0, 0, 0)),
        ("padding_top", "margin_top", 5, 0),
        ("padding_right", "margin_right", 5, 0),
        ("padding_bottom", "margin_bottom", 5, 0),
        ("padding_left", "margin_left", 5, 0),
    ],
)
@pytest.mark.parametrize("set_fn", (setattr, setitem))
@pytest.mark.parametrize("get_fn", (getattr, getitem))
@pytest.mark.parametrize("del_fn", (delattr, delitem))
def test_deprecated_properties(
    old_name, new_name, value, default, set_fn, get_fn, del_fn
):
    """Deprecated names alias to new names, and issue deprecation warnings."""
    # Set the old name, then check the new name.
    style = Pack()
    with pytest.warns(DeprecationWarning):
        set_fn(style, old_name, value)
    assert get_fn(style, new_name) == value

    # Delete the old name, check new name
    with pytest.warns(DeprecationWarning):
        del_fn(style, old_name)
    assert get_fn(style, new_name) == default

    # Set the new name, then check the old name.
    style = Pack()
    set_fn(style, new_name, value)
    with pytest.warns(DeprecationWarning):
        assert get_fn(style, old_name) == value

    # Delete the new name, check old name
    del_fn(style, new_name)
    with pytest.warns(DeprecationWarning):
        assert get_fn(style, old_name) == default


def test_padding_margin():
    """Padding aliases margin (but can't be checked with bracket notation)."""
    # Set the old name, then check the new name.
    style = Pack()
    with pytest.warns(DeprecationWarning):
        style.padding = (5, 5, 5, 5)
    assert style.margin == (5, 5, 5, 5)

    # Set the new name, then check the old name.
    style = Pack()
    style.margin = (5, 5, 5, 5)
    with pytest.warns(DeprecationWarning):
        assert style.padding == (5, 5, 5, 5)


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
def test_alignment_align_items(direction, text_direction, alignment, align_items):
    """Alignment (with deprecation warning) and align_items map to each other."""
    with pytest.warns(DeprecationWarning):
        style = Pack(
            direction=direction,
            text_direction=text_direction,
            alignment=alignment,
        )
    assert style.align_items == align_items

    with pytest.warns(DeprecationWarning):
        del style.alignment
    assert style.align_items is None

    style = Pack(
        direction=direction,
        text_direction=text_direction,
        align_items=align_items,
    )
    with pytest.warns(DeprecationWarning):
        assert style.alignment == alignment

    del style.align_items
    with pytest.warns(DeprecationWarning):
        assert style.alignment is None


@pytest.mark.parametrize(
    "direction, alignment",
    [
        (ROW, LEFT),
        (ROW, RIGHT),
        (COLUMN, TOP),
        (COLUMN, BOTTOM),
    ],
)
def test_alignment_align_items_invalid(direction, alignment):
    """Invalid settings for alignment should return None for align_items."""
    with pytest.warns(DeprecationWarning):
        style = Pack(direction=direction, alignment=alignment)
    assert style.align_items is None
