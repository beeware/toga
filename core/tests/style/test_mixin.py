import pytest
from pytest import raises

from toga.style import Pack

from ..utils import ExampleWidget


def test_constructor():
    """Style properties can be set with widget constructor kwargs."""
    widget = ExampleWidget()
    assert widget.id.isdigit()
    assert widget.style.flex == 0
    assert widget.style.display == "pack"

    widget = ExampleWidget(id="my-id", flex=1, display="none")
    assert widget.id == "my-id"
    assert widget.style.flex == 1
    assert widget.style.display == "none"

    with raises(NameError, match="Unknown style 'nonexistent'"):
        ExampleWidget(nonexistent=None)


def test_constructor_style():
    """If both a style object and kwargs are passed, the kwargs should take priority,
    and the style object should not be modified."""
    style = Pack(display="none", flex=1)
    widget = ExampleWidget(style=style, flex=2)
    assert widget.style.display == "none"
    assert widget.style.flex == 2
    assert style.flex == 1


def test_attribute():
    """Style properties can be accessed as widget properties."""
    widget = ExampleWidget()
    assert widget.flex == 0
    assert widget.style.flex == 0

    widget.flex = 1
    assert widget.flex == 1
    assert widget.style.flex == 1

    del widget.flex
    assert widget.flex == 0
    assert widget.style.flex == 0

    widget.style.flex = 2
    assert widget.flex == 2
    assert widget.style.flex == 2

    del widget.flex
    assert widget.flex == 0
    assert widget.style.flex == 0

    # Check regular attributes still work correctly
    with raises(AttributeError):
        widget.my_attr
    widget.my_attr = 42
    assert widget.my_attr == 42
    del widget.my_attr
    with raises(AttributeError):
        widget.my_attr


@pytest.mark.parametrize(
    "prop_name",
    # Make sure it works for both a plain property and a directional alias.
    ["flex", "margin"],
)
def test_class_attribute(prop_name):
    """Getting a style attribute from the class should return a property object."""
    prop = getattr(ExampleWidget, prop_name)
    assert type(prop).__name__ == "StyleProperty"
