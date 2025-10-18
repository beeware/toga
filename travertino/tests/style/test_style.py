import pytest

from travertino.properties.validated import list_property, validated_property

from .style_classes import (
    VALUE2,
    VALUE3,
    VALUES,
    DeprecatedStyle,
    Style,
)


def test_invalid_style():
    with pytest.raises(ValueError):
        # Define an invalid initial value on a validated property
        validated_property(*VALUES, integer=True, initial="something")

    with pytest.raises(ValueError):
        # Same for list property
        list_property(*VALUES, integer=True, initial=["something"])


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_positional_argument(StyleClass):
    # Could be the subclass or inherited __init__, depending on Python version / API
    # used.
    with pytest.raises(
        TypeError, match=r"__init__\(\) takes 1 positional argument but 2 were given"
    ):
        StyleClass(5)


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_constructor_invalid_property(StyleClass):
    """Whether dataclass or not, the error should be the same."""
    with pytest.raises(
        TypeError,
        match=r"Style\.__init__\(\) got an unexpected keyword argument 'bogus'",
    ):
        StyleClass(explicit_const=5, bogus=None)


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_create_and_copy(StyleClass):
    style = StyleClass(explicit_const=VALUE2, implicit=VALUE3)

    dup = style.copy()
    assert dup.explicit_const == VALUE2
    assert dup.explicit_value == 0
    assert dup.implicit == VALUE3


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_str(StyleClass):
    style = StyleClass()

    style.update(
        explicit_const=VALUE2,
        explicit_value=20,
        thing=(30, 40, 50, 60),
    )

    assert (
        str(style) == "explicit-const: value2; "
        "explicit-value: 20; "
        "thing-bottom: 50; "
        "thing-left: 60; "
        "thing-right: 40; "
        "thing-top: 30"
    )


def test_repr():
    # Doesn't need to be tested with deprecated API.
    style = Style(explicit_const=VALUE2, explicit_value=20, thing=(30, 40, 50, 60))

    assert repr(style) == (
        "Style("
        "explicit_const='value2', "
        "explicit_value=20, "
        "thing_bottom=50, "
        "thing_left=60, "
        "thing_right=40, "
        "thing_top=30"
        ")"
    )
