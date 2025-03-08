import pytest
from pytest import raises

from toga.style.pack import CENTER, COLUMN, END, ROW

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
    "css_name, row_alias, column_alias, default",
    [
        (
            "align_items",
            "vertical_align_items",
            "horizontal_align_items",
            None,
        ),
        (
            "justify_content",
            "horizontal_align_content",
            "vertical_align_content",
            "start",
        ),
    ],
)
@pytest.mark.parametrize(
    "style_with",
    (with_init, with_update, with_setattr, with_setitem, with_setitem_hyphen),
)
@pytest.mark.parametrize("get_fn", (getattr, getitem, getitem_hyphen))
@pytest.mark.parametrize("del_fn", (delattr, delitem, delitem_hyphen))
def test_align(css_name, row_alias, column_alias, default, style_with, get_fn, del_fn):
    """The `vertical_align` and `horizontal_align` aliases work correctly."""
    # Row alias
    style = style_with(**{row_alias: CENTER})
    assert_name_in(css_name, style)
    assert get_fn(style, css_name) == CENTER

    del_fn(style, row_alias)
    assert_name_not_in(css_name, style)
    assert get_fn(style, css_name) == default

    style = style_with(**{css_name: CENTER})
    assert_name_in(row_alias, style)
    assert get_fn(style, row_alias) == CENTER

    del_fn(style, css_name)
    assert_name_not_in(row_alias, style)
    assert get_fn(style, row_alias) == default

    # Column alias
    style = style_with(**{"direction": COLUMN, column_alias: CENTER})
    assert_name_in(css_name, style)
    assert get_fn(style, css_name) == CENTER

    del_fn(style, column_alias)
    assert_name_not_in(css_name, style)
    assert get_fn(style, css_name) == default

    style = style_with(**{"direction": COLUMN, css_name: CENTER})
    assert_name_in(column_alias, style)
    assert get_fn(style, column_alias) == CENTER

    del_fn(style, css_name)
    assert_name_not_in(column_alias, style)
    assert get_fn(style, column_alias) == default

    # Column alias is not accepted in a row, and vice versa.
    def assert_invalid_alias(alias, direction):
        style = style_with(direction=direction)
        correct_direction = ROW if direction == COLUMN else COLUMN
        raises_kwargs = dict(
            expected_exception=AttributeError,
            match=(
                rf"'{alias}' is only supported when "
                rf"\(direction == {correct_direction}\)"
            ),
        )

        with raises(**raises_kwargs):
            get_fn(style, alias)
        with raises(**raises_kwargs):
            setattr(style, alias, END)
        with raises(**raises_kwargs):
            del_fn(style, alias)
        with raises(**raises_kwargs):
            style.update(**{"direction": direction, alias: END})
        with raises(**raises_kwargs):
            style.update(**{alias: END, "direction": direction})
        with raises(**raises_kwargs):
            alias in style

    assert_invalid_alias(column_alias, ROW)
    assert_invalid_alias(row_alias, COLUMN)

    # Consistent values of direction and alias can be updated together, regardless of
    # argument order.
    style = style_with(direction=COLUMN)
    style.update(**{"direction": ROW, row_alias: CENTER})
    assert get_fn(style, row_alias) == CENTER
    assert get_fn(style, css_name) == CENTER
    style.update(**{column_alias: END, "direction": COLUMN})
    assert get_fn(style, column_alias) == END
    assert get_fn(style, css_name) == END

    style = style_with(direction=ROW)
    style.update(**{"direction": COLUMN, column_alias: CENTER})
    assert get_fn(style, column_alias) == CENTER
    assert get_fn(style, css_name) == CENTER
    style.update(**{row_alias: END, "direction": ROW})
    assert get_fn(style, row_alias) == END
    assert get_fn(style, css_name) == END
