import pytest

from toga.style.pack import Pack


def setitem(obj, name, value):
    obj[name] = value


def getitem(obj, name):
    return obj[name]


@pytest.mark.parametrize(
    "old_name, new_name, value",
    [
        # Travertino 0.3.0 doesn't support accessing a directional property via bracket
        # notation.
        # ("padding", "margin", (5, 5, 5, 5)),
        ("padding_top", "margin_top", 5),
        ("padding_right", "margin_right", 5),
        ("padding_bottom", "margin_bottom", 5),
        ("padding_left", "margin_left", 5),
        ("alignment", "align_items", "center"),
    ],
)
@pytest.mark.parametrize("set_fn", (setattr, setitem))
@pytest.mark.parametrize("get_fn", (getattr, getitem))
def test_deprecated_properties(old_name, new_name, value, set_fn, get_fn):
    """Deprecated names alias to new names, and issue deprecation warnings."""

    # Set the old name, then check the new name.
    style = Pack()
    with pytest.warns(DeprecationWarning):
        set_fn(style, old_name, value)
    assert get_fn(style, new_name) == value

    # Set the new name, then check the old name.
    style = Pack()
    set_fn(style, new_name, value)
    with pytest.warns(DeprecationWarning):
        assert get_fn(style, old_name) == value


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
