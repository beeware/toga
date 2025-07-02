from unittest.mock import call

import pytest

from .style_classes import DeprecatedStyle, Style


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
