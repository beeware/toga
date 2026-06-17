import pytest

from .style_classes import VALUE1, VALUE2, VALUE3, BaseStyle, DeprecatedStyle, Style


class StyleSubclass(Style):
    pass


class DeprecatedStyleSubclass(DeprecatedStyle):
    pass


class Sibling(BaseStyle):
    def _apply(self, names):
        pass

    def layout(self, viewport):
        pass


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
