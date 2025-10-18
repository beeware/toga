from unittest.mock import call

import pytest

from .style_classes import VALUE1, VALUE2, VALUE3, DeprecatedStyle, Style


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_apply(StyleClass):
    style = StyleClass(explicit_const=VALUE2, implicit=VALUE3)
    assert style.apply.mock_calls == [call("explicit_const"), call("implicit")]
    style.apply.reset_mock()

    style.apply()
    style.apply.assert_called_once_with()


@pytest.mark.parametrize(
    "name, initial",
    [
        ("explicit_const", VALUE1),
        ("explicit_value", 0),
        ("explicit_none", None),
        ("implicit", None),
    ],
)
@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_property(name, initial, StyleClass):
    style = StyleClass()

    # Default value
    assert style[name] == initial
    style.apply.assert_not_called()

    # Modify the value
    style[name] = 10

    assert style[name] == 10
    style.apply.assert_called_once_with(name)

    # Clear the applicator mock
    style.apply.reset_mock()

    # Set the value to the same value.
    # No dirty notification is sent
    style[name] = 10
    assert style[name] == 10
    style.apply.assert_not_called()

    # Set the value to something new
    # A dirty notification is set.
    style[name] = 20
    assert style[name] == 20
    style.apply.assert_called_once_with(name)

    # Clear the applicator mock
    style.apply.reset_mock()

    # Clear the property
    del style[name]
    assert style[name] == initial
    style.apply.assert_called_once_with(name)

    # Clear the applicator mock
    style.apply.reset_mock()

    # Clear the property again.
    # The underlying attribute won't exist, so this should be a no-op.
    del style[name]
    assert style[name] is initial
    style.apply.assert_not_called()


@pytest.mark.parametrize("StyleClass", [Style, DeprecatedStyle])
def test_set_delete_initial_no_apply(StyleClass):
    """Assigning or deleting a value equal to the initial value shouldn't apply."""
    style = StyleClass()

    # 0 is the initial value
    style.explicit_value = 0
    style.apply.assert_not_called()

    del style.explicit_value
    style.apply.assert_not_called()


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
