from __future__ import annotations

from collections.abc import Sequence
from unittest.mock import call
from warnings import catch_warnings, filterwarnings

import pytest

from travertino.properties.choices import Choices
from travertino.properties.immutablelist import ImmutableList
from travertino.properties.shorthand import directional_property
from travertino.properties.validated import list_property, validated_property
from travertino.style import BaseStyle

from .utils import apply_dataclass, mock_apply

VALUE1 = "value1"
VALUE2 = "value2"
VALUE3 = "value3"
VALUES = [VALUE1, VALUE2, VALUE3, None]


@mock_apply
@apply_dataclass
class Style(BaseStyle):
    # Some properties with explicit initial values
    explicit_const: str | int = validated_property(
        *VALUES, integer=True, initial=VALUE1
    )
    explicit_value: str | int = validated_property(*VALUES, integer=True, initial=0)
    explicit_none: str | int | None = validated_property(
        *VALUES, integer=True, initial=None
    )

    # A property with an implicit default value.
    # This usually means the default is platform specific.
    implicit: str | int | None = validated_property(
        VALUE1, VALUE2, VALUE3, integer=True
    )

    # A set of directional properties
    thing: tuple[str | int] | str | int = directional_property("thing{}")
    thing_top: str | int = validated_property(*VALUES, integer=True, initial=0)
    thing_right: str | int = validated_property(*VALUES, integer=True, initial=0)
    thing_bottom: str | int = validated_property(*VALUES, integer=True, initial=0)
    thing_left: str | int = validated_property(*VALUES, integer=True, initial=0)

    # Doesn't need to be tested in deprecated API:
    list_prop: list[str] = list_property(*VALUES, integer=True, initial=(VALUE2,))


VALUE_CHOICES = Choices(*VALUES, integer=True)

with catch_warnings():
    filterwarnings("ignore", category=DeprecationWarning)

    @mock_apply
    class DeprecatedStyle(BaseStyle):
        pass

    # Some properties with explicit initial values
    DeprecatedStyle.validated_property(
        "explicit_const", choices=VALUE_CHOICES, initial=VALUE1
    )
    DeprecatedStyle.validated_property(
        "explicit_value", choices=VALUE_CHOICES, initial=0
    )
    DeprecatedStyle.validated_property(
        "explicit_none", choices=VALUE_CHOICES, initial=None
    )

    # A property with an implicit default value.
    # This usually means the default is platform specific.
    DeprecatedStyle.validated_property(
        "implicit", choices=Choices(VALUE1, VALUE2, VALUE3, integer=True)
    )

    # A set of directional properties
    DeprecatedStyle.validated_property("thing_top", choices=VALUE_CHOICES, initial=0)
    DeprecatedStyle.validated_property("thing_right", choices=VALUE_CHOICES, initial=0)
    DeprecatedStyle.validated_property("thing_bottom", choices=VALUE_CHOICES, initial=0)
    DeprecatedStyle.validated_property("thing_left", choices=VALUE_CHOICES, initial=0)
    DeprecatedStyle.directional_property("thing%s")


class StyleSubclass(Style):
    pass


class DeprecatedStyleSubclass(DeprecatedStyle):
    pass


class Sibling(BaseStyle):
    pass


@mock_apply
@apply_dataclass
class MockedApplyStyle(BaseStyle):
    pass


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
def test_create_and_copy(StyleClass):
    style = StyleClass(explicit_const=VALUE2, implicit=VALUE3)

    dup = style.copy()
    assert dup.explicit_const == VALUE2
    assert dup.explicit_value == 0
    assert dup.implicit == VALUE3


def test_deprecated_copy():
    style = MockedApplyStyle()

    with pytest.warns(DeprecationWarning):
        style_copy = style.copy(applicator=object())

    style_copy.apply.assert_called_once_with()


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_apply(StyleClass):
    style = StyleClass(explicit_const=VALUE2, implicit=VALUE3)
    assert style.apply.mock_calls == [call("explicit_const"), call("implicit")]
    style.apply.reset_mock()

    style.apply()
    style.apply.assert_called_once_with()


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_property_with_explicit_const(StyleClass):
    style = StyleClass()

    # Default value is VALUE1
    assert style.explicit_const is VALUE1
    style.apply.assert_not_called()

    # Modify the value
    style.explicit_const = 10

    assert style.explicit_const == 10
    style.apply.assert_called_once_with("explicit_const")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set the value to the same value.
    # No dirty notification is sent
    style.explicit_const = 10
    assert style.explicit_const == 10
    style.apply.assert_not_called()

    # Set the value to something new
    # A dirty notification is set.
    style.explicit_const = 20
    assert style.explicit_const == 20
    style.apply.assert_called_once_with("explicit_const")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Clear the property
    del style.explicit_const
    assert style.explicit_const is VALUE1
    style.apply.assert_called_once_with("explicit_const")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Clear the property again.
    # The underlying attribute won't exist, so this
    # should be a no-op.
    del style.explicit_const
    assert style.explicit_const is VALUE1
    style.apply.assert_not_called()


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_property_with_explicit_value(StyleClass):
    style = StyleClass()

    # Default value is 0
    assert style.explicit_value == 0
    style.apply.assert_not_called()

    # Modify the value
    style.explicit_value = 10

    assert style.explicit_value == 10
    style.apply.assert_called_once_with("explicit_value")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set the value to the same value.
    # No dirty notification is sent
    style.explicit_value = 10
    assert style.explicit_value == 10
    style.apply.assert_not_called()

    # Set the value to something new
    # A dirty notification is set.
    style.explicit_value = 20
    assert style.explicit_value == 20
    style.apply.assert_called_once_with("explicit_value")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Clear the property
    del style.explicit_value
    assert style.explicit_value == 0
    style.apply.assert_called_once_with("explicit_value")


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_property_with_explicit_none(StyleClass):
    style = StyleClass()

    # Default value is None
    assert style.explicit_none is None
    style.apply.assert_not_called()

    # Modify the value
    style.explicit_none = 10

    assert style.explicit_none == 10
    style.apply.assert_called_once_with("explicit_none")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set the property to the same value.
    # No dirty notification is sent
    style.explicit_none = 10
    assert style.explicit_none == 10
    style.apply.assert_not_called()

    # Set the property to something new
    # A dirty notification is set.
    style.explicit_none = 20
    assert style.explicit_none == 20
    style.apply.assert_called_once_with("explicit_none")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Clear the property
    del style.explicit_none
    assert style.explicit_none is None
    style.apply.assert_called_once_with("explicit_none")


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_property_with_implicit_default(StyleClass):
    style = StyleClass()

    # Default value is None
    assert style.implicit is None
    style.apply.assert_not_called()

    # Modify the value
    style.implicit = 10

    assert style.implicit == 10
    style.apply.assert_called_once_with("implicit")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set the value to the same value.
    # No dirty notification is sent
    style.implicit = 10
    assert style.implicit == 10
    style.apply.assert_not_called()

    # Set the value to something new
    # A dirty notification is set.
    style.implicit = 20
    assert style.implicit == 20
    style.apply.assert_called_once_with("implicit")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Clear the property
    del style.implicit
    assert style.implicit is None
    style.apply.assert_called_once_with("implicit")


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_set_initial_no_apply(StyleClass):
    """If a property hasn't been set, assigning it its initial value shouldn't apply."""
    style = StyleClass()

    # 0 is the initial value
    style.explicit_value = 0

    style.apply.assert_not_called()


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_directional_property(StyleClass):
    style = StyleClass()

    # Default value is 0
    assert style.thing == (0, 0, 0, 0)
    assert style.thing_top == 0
    assert style.thing_right == 0
    assert style.thing_bottom == 0
    assert style.thing_left == 0
    assert "thing" not in style
    style.apply.assert_not_called()

    # Set a value in one axis
    style.thing_top = 10

    assert style.thing == (10, 0, 0, 0)
    assert style.thing_top == 10
    assert style.thing_right == 0
    assert style.thing_bottom == 0
    assert style.thing_left == 0
    assert "thing" in style
    style.apply.assert_called_once_with("thing_top")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set a value directly with a single item
    style.thing = (10,)

    assert style.thing == (10, 10, 10, 10)
    assert style.thing_top == 10
    assert style.thing_right == 10
    assert style.thing_bottom == 10
    assert style.thing_left == 10
    assert "thing" in style
    style.apply.assert_has_calls(
        [
            call("thing_right"),
            call("thing_bottom"),
            call("thing_left"),
        ]
    )

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set a value directly with a single item
    style.thing = 30

    assert style.thing == (30, 30, 30, 30)
    assert style.thing_top == 30
    assert style.thing_right == 30
    assert style.thing_bottom == 30
    assert style.thing_left == 30
    assert "thing" in style
    style.apply.assert_has_calls(
        [
            call("thing_top"),
            call("thing_right"),
            call("thing_bottom"),
            call("thing_left"),
        ]
    )

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set a value directly with 2 values
    style.thing = (10, 20)

    assert style.thing == (10, 20, 10, 20)
    assert style.thing_top == 10
    assert style.thing_right == 20
    assert style.thing_bottom == 10
    assert style.thing_left == 20
    assert "thing" in style
    style.apply.assert_has_calls(
        [
            call("thing_top"),
            call("thing_right"),
            call("thing_bottom"),
            call("thing_left"),
        ]
    )

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set a value directly with 3 values
    style.thing = (10, 20, 30)

    assert style.thing == (10, 20, 30, 20)
    assert style.thing_top == 10
    assert style.thing_right == 20
    assert style.thing_bottom == 30
    assert style.thing_left == 20
    assert "thing" in style
    style.apply.assert_called_once_with("thing_bottom")

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set a value directly with 4 values
    style.thing = (10, 20, 30, 40)

    assert style.thing == (10, 20, 30, 40)
    assert style.thing_top == 10
    assert style.thing_right == 20
    assert style.thing_bottom == 30
    assert style.thing_left == 40
    assert "thing" in style
    style.apply.assert_called_once_with("thing_left")

    # Set a value directly with an invalid number of values
    with pytest.raises(ValueError):
        style.thing = ()

    with pytest.raises(ValueError):
        style.thing = (10, 20, 30, 40, 50)

    # Clear the applicator mock
    style.apply.reset_mock()

    # Clear a value on one axis
    del style.thing_top

    assert style.thing == (0, 20, 30, 40)
    assert style.thing_top == 0
    assert style.thing_right == 20
    assert style.thing_bottom == 30
    assert style.thing_left == 40
    assert "thing" in style
    style.apply.assert_called_once_with("thing_top")

    # Restore the top thing
    style.thing_top = 10

    # Clear the applicator mock
    style.apply.reset_mock()

    # Clear a value directly
    del style.thing

    assert style.thing == (0, 0, 0, 0)
    assert style.thing_top == 0
    assert style.thing_right == 0
    assert style.thing_bottom == 0
    assert style.thing_left == 0
    assert "thing" not in style
    style.apply.assert_has_calls(
        [
            call("thing_right"),
            call("thing_bottom"),
            call("thing_left"),
        ]
    )


@pytest.mark.parametrize(
    "value, expected",
    [
        ([VALUE1], [VALUE1]),
        (VALUE1, [VALUE1]),
        ([VALUE1, VALUE3], [VALUE1, VALUE3]),
        ([VALUE2, VALUE1], [VALUE2, VALUE1]),
        ([VALUE2, VALUE3, 1, 2, VALUE1], [VALUE2, VALUE3, 1, 2, VALUE1]),
        # Duplicates are kept, but "normalized" via validation.
        (
            [VALUE3, 1, VALUE3, "1", True, " 1", VALUE2],
            [VALUE3, 1, VALUE3, 1, 1, 1, VALUE2],
        ),
        # Other sequences should work too.
        ((VALUE1, VALUE3), [VALUE1, VALUE3]),
    ],
)
def test_list_property(value, expected):
    style = Style()
    style.list_prop = value
    assert style.list_prop == expected


@pytest.mark.parametrize(
    "value, error, match",
    [
        (
            5,
            TypeError,
            r"Value for list property list_prop must be a sequence\.",
        ),
        (
            # Fails because it's only a generator, not a comprehension:
            (i for i in [VALUE1, VALUE3]),
            TypeError,
            r"Value for list property list_prop must be a sequence.",
        ),
        (
            [VALUE3, VALUE1, "bogus"],
            ValueError,
            r"Invalid item value 'bogus' for list property list_prop; "
            r"Valid values are: none, value1, value2, value3, <integer>",
        ),
        (
            (),
            ValueError,
            r"List properties cannot be set to an empty sequence; "
            r"to reset a property, use del `style.list_prop`\.",
        ),
        (
            [],
            ValueError,
            r"List properties cannot be set to an empty sequence; "
            r"to reset a property, use del `style.list_prop`\.",
        ),
    ],
)
def test_list_property_invalid(value, error, match):
    style = Style()
    with pytest.raises(error, match=match):
        style.list_prop = value


def test_list_property_immutable():
    style = Style()
    style.list_prop = [1, 2, 3, VALUE2]
    prop = style.list_prop

    with pytest.raises(TypeError, match=r"does not support item assignment"):
        prop[0] = 5

    with pytest.raises(TypeError, match=r"doesn't support item deletion"):
        del prop[1]

    with pytest.raises(AttributeError):
        prop.insert(2, VALUE1)

    with pytest.raises(AttributeError):
        prop.append(VALUE3)

    with pytest.raises(AttributeError):
        prop.clear()

    with pytest.raises(AttributeError):
        prop.reverse()

    with pytest.raises(AttributeError):
        prop.pop()

    with pytest.raises(AttributeError):
        prop.remove(VALUE2)

    with pytest.raises(AttributeError):
        prop.extend([5, 6, 7])

    with pytest.raises(TypeError, match=r"unsupported operand type\(s\)"):
        prop += [4, 3, VALUE1]

    with pytest.raises(TypeError, match=r"unsupported operand type\(s\)"):
        prop += ImmutableList([4, 3, VALUE1])

    with pytest.raises(AttributeError):
        prop.sort()


def test_list_property_list_like():
    style = Style()
    style.list_prop = [1, 2, 3, VALUE2]
    prop = style.list_prop

    assert isinstance(prop, ImmutableList)
    assert prop == [1, 2, 3, VALUE2]
    assert prop == ImmutableList([1, 2, 3, VALUE2])
    assert prop[2] == 3
    assert str(prop) == repr(prop) == "[1, 2, 3, 'value2']"
    assert len(prop) == 4

    count = 0
    for _ in prop:
        count += 1
    assert count == 4

    assert [*reversed(prop)] == [VALUE2, 3, 2, 1]

    assert prop.index(3) == 2

    assert prop.count(VALUE2) == 1

    assert isinstance(prop, Sequence)


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_set_multiple_properties(StyleClass):
    style = StyleClass()

    # Set a pair of properties
    style.update(explicit_value=20, explicit_none=10)

    assert style.explicit_const is VALUE1
    assert style.explicit_none == 10
    assert style.explicit_value == 20
    style.apply.assert_has_calls(
        [
            call("explicit_value"),
            call("explicit_none"),
        ],
        any_order=True,
    )

    # Set a different pair of properties
    style.update(explicit_const=VALUE2, explicit_value=30)

    assert style.explicit_const is VALUE2
    assert style.explicit_value == 30
    assert style.explicit_none == 10
    style.apply.assert_has_calls(
        [
            call("explicit_const"),
            call("explicit_value"),
        ],
        any_order=True,
    )

    # Clear the applicator mock
    style.apply.reset_mock()

    # Setting a non-property
    with pytest.raises(NameError):
        style.update(not_a_property=10)

    style.apply.assert_not_called()


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


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_dict(StyleClass):
    "Style declarations expose a dict-like interface"
    style = StyleClass()

    style.update(
        explicit_const=VALUE2,
        explicit_value=20,
        thing=(30, 40, 50, 60),
    )

    expected_keys = {
        "explicit_const",
        "explicit_value",
        "thing_bottom",
        "thing_left",
        "thing_right",
        "thing_top",
    }

    assert style.keys() == expected_keys

    assert sorted(style.items()) == sorted(
        [
            ("explicit_const", "value2"),
            ("explicit_value", 20),
            ("thing_bottom", 50),
            ("thing_left", 60),
            ("thing_right", 40),
            ("thing_top", 30),
        ]
    )

    # Style object has a length and is iterable.
    assert len(style) == 6
    for name in style:
        assert name in expected_keys

    # Properties that are set are in the keys.
    for name in expected_keys:
        assert name in style

    # Directional properties with one or more of the aliased properties set also count.
    assert "thing" in style

    # Valid properties that haven't been set are not in the keys.
    assert "implicit" not in style
    assert "explicit_none" not in style

    # Neither are invalid properties.
    assert "invalid_property" not in style

    # A property can be set, retrieved and cleared using the attribute name
    style["thing-bottom"] = 10
    assert style["thing-bottom"] == 10
    del style["thing-bottom"]
    assert style["thing-bottom"] == 0

    # A property can be set, retrieved and cleared using the Python attribute name
    style["thing_bottom"] = 10
    assert style["thing_bottom"] == 10
    del style["thing_bottom"]
    assert style["thing_bottom"] == 0

    # Property aliases can be accessed as well.
    style["thing"] = 5
    assert style["thing"] == (5, 5, 5, 5)
    del style["thing"]
    assert style["thing"] == (0, 0, 0, 0)

    # Clearing a valid property isn't an error
    del style["thing_bottom"]
    assert style["thing_bottom"] == 0

    # Non-existent properties raise KeyError
    with pytest.raises(KeyError):
        style["no-such-property"] = "no-such-value"

    with pytest.raises(KeyError):
        style["no-such-property"]

    with pytest.raises(KeyError):
        del style["no-such-property"]


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_set_to_initial(StyleClass):
    """A property set to its initial value is distinct from an unset property."""
    style = StyleClass()

    # explicit_const's initial value is VALUE1.
    assert style.explicit_const == VALUE1
    assert "explicit_const" not in style

    # The unset property shouldn't affect the value when overlaid over a style with
    # that property set.
    non_initial_style = StyleClass(explicit_const=VALUE2)
    union = non_initial_style | style
    assert union.explicit_const == VALUE2
    assert "explicit_const" in union

    # The property should count as set, even when set to the same initial value.
    style.explicit_const = VALUE1
    assert style.explicit_const == VALUE1
    assert "explicit_const" in style

    # The property should now overwrite.
    union = non_initial_style | style
    assert union.explicit_const == VALUE1
    assert "explicit_const" in union


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
@pytest.mark.parametrize("instantiate", [True, False])
def test_union_operators(StyleClass, instantiate):
    """Styles support | and |= with dicts and with their own class."""
    left = StyleClass(explicit_value=VALUE1, implicit=VALUE2)

    style_dict = {"thing_top": 5, "implicit": VALUE3}
    right = StyleClass(**style_dict) if instantiate else style_dict

    # Standard operator
    result = left | right

    # Original objects unchanged
    assert left["explicit_value"] == VALUE1
    assert left["implicit"] == VALUE2

    assert right["thing_top"] == 5
    assert right["implicit"] == VALUE3

    # Unshared properties assigned
    assert result["explicit_const"] == VALUE1
    assert result["thing_top"] == 5

    # Common property overridden by second operand
    assert result["implicit"] == VALUE3

    # In-place version
    left |= right

    # Common property updated on lefthand
    assert left["explicit_value"] == VALUE1
    assert left["implicit"] == VALUE3

    # Righthand unchanged
    assert right["thing_top"] == 5
    assert right["implicit"] == VALUE3


@pytest.mark.parametrize(
    "StyleClass, OtherClass",
    [
        (Style, StyleSubclass),
        (Style, Sibling),
        (Style, int),
        (Style, list),
        (DeprecatedStyle, DeprecatedStyleSubclass),
        (DeprecatedStyle, Sibling),
        (DeprecatedStyle, int),
        (DeprecatedStyle, list),
    ],
)
def test_union_operators_invalid_type(StyleClass, OtherClass):
    """Styles do not support | or |= with other style classes or with non-mappings."""

    left = StyleClass()
    right = OtherClass()

    with pytest.raises(TypeError, match=r"unsupported operand type"):
        left | right

    with pytest.raises(TypeError, match=r"unsupported operand type"):
        left |= right


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
@pytest.mark.parametrize(
    "right, error",
    [
        ({"implicit": "bogus_value"}, ValueError),
        ({"bogus_key": 3.12}, NameError),
    ],
)
def test_union_operators_invalid_key_value(StyleClass, right, error):
    """Operators will accept any mapping, but invalid keys/values are still an error."""
    left = StyleClass()

    with pytest.raises(error):
        left | right

    with pytest.raises(error):
        left |= right


def test_deprecated_class_methods():
    class OldStyle(BaseStyle):
        pass

    with pytest.warns(DeprecationWarning):
        OldStyle.validated_property(
            "implicit", Choices(*VALUES, integer=True), initial=VALUE1
        )

    with pytest.warns(DeprecationWarning):
        OldStyle.directional_property("thing%s")


def test_deprecated_reapply():
    """Reapply() is deprecated (but still calls apply()."""
    style = Style()
    with pytest.warns(DeprecationWarning):
        style.reapply()

    style.apply.assert_called_once_with()


def test_deprecated_import():
    with pytest.deprecated_call():
        from travertino.declaration import BaseStyle, Choices  # noqa
