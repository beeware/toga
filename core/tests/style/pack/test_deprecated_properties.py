import pytest

from toga.style.pack import Pack


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
        ("alignment", "align_items", "center", None),
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
    """Padding aliases margin, but can't be checked with bracket notation."""

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
