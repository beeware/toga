import pytest
from pytest import raises

from toga.style import Pack

from ..utils import ExampleWidget

params = (
    "name, value, default",
    [
        ("flex", 1, 0),  # Regular style
        ("horizontal_align_content", "center", "start"),  # Style alias
    ],
)


@pytest.mark.parametrize(*params)
def test_constructor(name, value, default):
    """Style properties can be set with widget constructor kwargs."""
    widget = ExampleWidget()
    assert widget.id.isdigit()
    assert getattr(widget.style, name) == default
    assert widget.style.display == "pack"

    widget = ExampleWidget(**{"id": "my-id", name: value, "display": "none"})
    assert widget.id == "my-id"
    assert getattr(widget.style, name) == value
    assert widget.style.display == "none"

    with raises(
        TypeError,
        match=r"Pack\.__init__\(\) got an unexpected keyword argument 'nonexistent'",
    ):
        ExampleWidget(nonexistent=None)


@pytest.mark.parametrize(*params)
def test_constructor_style(name, value, default):
    """If both a style object and kwargs are passed, the kwargs should take priority,
    and the style object should not be modified."""
    style = Pack(**{"display": "none", name: default})
    widget = ExampleWidget(**{"style": style, name: value})
    assert widget.style.display == "none"
    assert getattr(widget.style, name) == value
    assert getattr(style, name) == default


@pytest.mark.parametrize(*params)
def test_attribute(name, value, default):
    """Style properties can be accessed as widget properties."""
    widget = ExampleWidget()
    assert getattr(widget, name) == default
    assert getattr(widget.style, name) == default

    setattr(widget, name, value)
    assert getattr(widget, name) == value
    assert getattr(widget.style, name) == value

    delattr(widget, name)
    assert getattr(widget, name) == default
    assert getattr(widget.style, name) == default

    setattr(widget.style, name, value)
    assert getattr(widget, name) == value
    assert getattr(widget.style, name) == value

    delattr(widget.style, name)
    assert getattr(widget, name) == default
    assert getattr(widget.style, name) == default


def test_regular_attribute():
    """Regular attributes still work correctly."""
    widget = ExampleWidget()
    with raises(AttributeError):
        widget.my_attr
    widget.my_attr = 42
    assert widget.my_attr == 42
    del widget.my_attr
    with raises(AttributeError):
        widget.my_attr


@pytest.mark.parametrize(*params)
def test_class_attribute(name, value, default):
    """Getting a style attribute from the class should return a property object."""
    prop = getattr(ExampleWidget, name)
    assert repr(prop) == f"<StyleProperty '{name}'>"
