import pytest

from .style_classes import VALUE1, VALUE2, VALUE3, VALUE4, Style


def test_default_values():
    """Shorthand property returns the initial defaults."""
    style = Style()
    assert style.composite_no_optional == (VALUE1, 0)
    assert style.composite_optional == (None, VALUE2, VALUE1, 0)


@pytest.mark.parametrize(
    "prop_name, min_num, max_num, match",
    [
        (
            "composite_no_optional",
            2,
            2,
            (
                r"Composite property 'composite_no_optional' assignment must provide "
                r"'explicit_const' and 'explicit_value'\."
            ),
        ),
        (
            "composite_optional",
            2,
            4,
            (
                r"Composite property 'composite_optional' assignment must provide "
                r"'explicit_const' and 'explicit_value', optionally preceded by "
                r"'explicit_none' and/or 'different_values_prop'\."
            ),
        ),
        (
            "composite_different_lengths",
            1,
            4,
            (
                r"Composite property 'composite_different_lengths' assignment must "
                r"provide 'explicit_value', optionally preceded by 'explicit_none', "
                r"'different_values_prop', and/or 'explicit_const'\."
            ),
        ),
    ],
)
def test_wrong_number_args(prop_name, min_num, max_num, match):
    """Too many or not enough values raises an error."""
    for num_values in [min_num - 1, max_num + 1]:
        values = (VALUE1,) * num_values

        with pytest.raises(TypeError, match=match):
            _ = Style(**{prop_name: values})


@pytest.mark.parametrize(
    "value",
    [
        "I'm a string",
        42,
        None,
    ],
)
def test_invalid_value(value):
    """Assigning a string or a non-sequence also raises an error."""
    with pytest.raises(
        TypeError,
        match=(
            r"Composite property 'composite_no_optional' assignment must provide "
            r"'explicit_const' and 'explicit_value'\."
        ),
    ):
        _ = Style(composite_no_optional=value)


def test_set_composite_with_no_optionals():
    """Values can be set and retrieved on a shorthand with only required properties."""
    style = Style(composite_no_optional=(VALUE2, VALUE3))
    assert style.composite_no_optional == (VALUE2, VALUE3)
    assert style.explicit_const == VALUE2
    assert style.explicit_value == VALUE3


# The following all test the logic involved with optional properties.


def assert_composite(style, expected):
    # Test against retrieving the composite property
    assert style.composite_optional == expected

    # Also test against the referenced properties directly.
    (explicit_none, different_values_prop, explicit_const, explicit_value) = expected
    assert style.explicit_none == explicit_none
    assert style.different_values_prop == different_values_prop
    assert style.explicit_const == explicit_const
    assert style.explicit_value == explicit_value


def test_assign_only_requied():
    """Assigning only the required properties works."""
    style = Style(composite_optional=(VALUE2, VALUE3))

    # The two optional properties should still be their default values.
    assert_composite(style, (None, VALUE2, VALUE2, VALUE3))
    # Confirm that they haven't been explicitly set.
    assert "different_values_prop" not in style
    assert "explicit_none" not in style


@pytest.mark.parametrize(
    "values",
    [
        # Both optional properties can accept VALUE1, VALUE2, and VALUE3; however, only
        # explicit_none can accept integers, and only different_values_prop can accept
        # VALUE4.
        (5, VALUE4, VALUE2, VALUE3),
        # Should also work with optionals reordered
        (VALUE4, 5, VALUE2, VALUE3),
    ],
)
def test_assign_all_non_default(values):
    """Assigning both optionals works, regardless of order."""
    style = Style(composite_optional=values)
    assert_composite(style, (5, VALUE4, VALUE2, VALUE3))


def test_assign_all_overlapping_values():
    """When both optionals can accept the values, they're assigned in order."""
    style = Style(composite_optional=(VALUE1, VALUE3, VALUE2, VALUE3))
    assert_composite(style, (VALUE1, VALUE3, VALUE2, VALUE3))


@pytest.mark.parametrize(
    "values",
    [
        # Default: (None, VALUE2, VALUE1, 0)
        # 5 is nondefault, VALUE2 is default
        # Optionals in order
        (5, VALUE2, VALUE2, VALUE3),
        # Optionals out of order
        (VALUE2, 5, VALUE2, VALUE3),
        # (Can't test setting explicit_none to its default, since it's None)
    ],
)
def test_assign_all_one_optional_non_default(values):
    """Full assignment setting one optional to a non-default works."""
    style = Style(composite_optional=values)
    assert_composite(style, (5, VALUE2, VALUE2, VALUE3))


ONE_OPTIONAL_NON_DEFAULT_PARAMS = pytest.mark.parametrize(
    "values, expected, unassigned_prop",
    [
        # Assign 5 to explicit_none, don't provide different_values_prop.
        (
            (5, VALUE2, VALUE3),
            (5, VALUE2, VALUE2, VALUE3),
            "different_values_prop",
        ),
        # Assign VALUE4 to different_values_prop, don't provide explicit_none.
        (
            (VALUE4, VALUE2, VALUE3),
            (None, VALUE4, VALUE2, VALUE3),
            "explicit_none",
        ),
    ],
)


@ONE_OPTIONAL_NON_DEFAULT_PARAMS
def test_assign_one_optional_non_default(values, expected, unassigned_prop):
    """One optional can be set to a non-default without specifying the other."""
    style = Style(composite_optional=values)
    assert_composite(style, expected)
    assert unassigned_prop not in style


@ONE_OPTIONAL_NON_DEFAULT_PARAMS
def test_assign_one_non_default_after_setting(values, expected, unassigned_prop):
    """Omitting an optional unsets it, even if it's been previously set."""
    style = Style()
    style[unassigned_prop] = VALUE2
    style.composite_optional = values

    assert_composite(style, expected)
    assert unassigned_prop not in style


def test_assign_invalid_optional_prop():
    """A value that's invalid for all optional properties raises an error."""
    with pytest.raises(
        ValueError,
        match=(
            r"Value 'bogus' not valid for any optional properties of composite "
            r"property 'composite_optional'"
        ),
    ):
        _ = Style(composite_optional=("bogus", VALUE2, VALUE3))


def test_assign_invalid_no_optionals_remaining():
    """A value raises an error if it's valid only for a property already filled."""
    with pytest.raises(
        ValueError,
        match=(
            r"Value 10 not valid for any optional properties of composite property "
            r"'composite_optional' that are not already being assigned"
        ),
    ):
        _ = Style(composite_optional=(10, 10, VALUE2, VALUE3))
