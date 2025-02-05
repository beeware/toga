import re

import pytest

from travertino.colors import hsl, hsla, rgb, rgba

from ..utils import assert_equal_color


@pytest.mark.parametrize(
    "front_color, back_color, expected_blended_color",
    [
        # Test with rgba color inputs:
        #
        # Black, gray, white front colors
        (rgba(0, 0, 0, 0), rgba(0, 0, 0, 0), rgba(0, 0, 0, 0)),
        (rgba(0, 0, 0, 0), rgba(50, 128, 200, 1.0), rgba(50, 128, 200, 1)),
        (rgba(0, 0, 0, 1.0), rgba(50, 128, 200, 0.9), rgba(0, 0, 0, 1.0)),
        (rgba(128, 128, 128, 1.0), rgba(50, 128, 200, 0.5), rgba(128, 128, 128, 1.0)),
        (rgba(255, 255, 255, 1.0), rgba(50, 128, 200, 0.0), rgba(255, 255, 255, 1.0)),
        # Primaries
        (rgba(255, 0, 0, 1.0), rgba(0, 255, 0, 1.0), rgba(255, 0, 0, 1.0)),
        (rgba(0, 255, 0, 1.0), rgba(255, 0, 0, 1.0), rgba(0, 255, 0, 1.0)),
        (rgba(0, 0, 255, 1.0), rgba(255, 0, 0, 1.0), rgba(0, 0, 255, 1.0)),
        # Color with different channel values, including transparency
        (rgba(50, 128, 200, 0.0), rgba(255, 255, 255, 1.0), rgba(255, 255, 255, 1)),
        (rgba(50, 128, 200, 0.5), rgba(128, 128, 128, 1.0), rgba(89, 128, 164, 1)),
        (rgba(50, 128, 200, 0.9), rgba(0, 0, 0, 1.0), rgba(45, 115, 180, 1)),
        (rgba(50, 128, 200, 1.0), rgba(0, 0, 0, 0), rgba(50, 128, 200, 1.0)),
        # Both front_color and back_color having intermediate alpha
        (
            rgba(100, 200, 255, 0.15),
            rgba(255, 100, 200, 0.85),
            rgba(228, 117, 209, 0.87),
        ),
        (rgba(120, 180, 240, 0.2), rgba(240, 120, 180, 0.8), rgba(211, 134, 194, 0.84)),
        (rgba(150, 50, 100, 0.4), rgba(100, 150, 50, 0.6), rgba(126, 97, 76, 0.76)),
        (rgba(50, 60, 70, 0.55), rgba(70, 80, 90, 0.45), rgba(55, 65, 75, 0.75)),
        (rgba(255, 255, 0, 0.3), rgba(0, 255, 255, 0.7), rgba(97, 255, 158, 0.79)),
        #
        # Test with rgb color inputs:
        #
        # Black, gray, white front colors
        (rgb(0, 0, 0), rgb(0, 0, 0), rgba(0, 0, 0, 1.0)),
        (rgb(0, 0, 0), rgb(50, 128, 200), rgba(0, 0, 0, 1.0)),
        (rgb(128, 128, 128), rgb(50, 128, 200), rgba(128, 128, 128, 1.0)),
        (rgb(255, 255, 255), rgb(50, 128, 200), rgba(255, 255, 255, 1.0)),
        # Primaries
        (rgb(255, 0, 0), rgb(0, 255, 0), rgba(255, 0, 0, 1.0)),
        (rgb(0, 255, 0), rgb(255, 0, 0), rgba(0, 255, 0, 1.0)),
        (rgb(0, 0, 255), rgb(255, 0, 0), rgba(0, 0, 255, 1.0)),
        # Color with different channel values
        (rgb(50, 128, 200), rgb(255, 255, 255), rgba(50, 128, 200, 1.0)),
        (rgb(50, 128, 200), rgb(128, 128, 128), rgba(50, 128, 200, 1.0)),
        (rgb(50, 128, 200), rgb(0, 0, 0), rgba(50, 128, 200, 1.0)),
        # Both front_color and back_color having intermediate values
        (rgb(100, 200, 255), rgb(255, 100, 200), rgba(100, 200, 255, 1.0)),
        (rgb(120, 180, 240), rgb(240, 120, 180), rgba(120, 180, 240, 1.0)),
        (rgb(150, 50, 100), rgb(100, 150, 50), rgba(150, 50, 100, 1.0)),
        (rgb(50, 60, 70), rgb(70, 80, 90), rgba(50, 60, 70, 1.0)),
        (rgb(255, 255, 0), rgb(0, 255, 255), rgba(255, 255, 0, 1.0)),
        #
        # Test with hsla color inputs:
        #
        # Black, gray, white front colors
        (hsla(0, 0, 0, 0), hsla(0, 0, 0, 0), rgba(0, 0, 0, 0)),
        (hsla(0, 0, 0, 0), hsla(208.8, 0.6, 0.49, 1.0), rgba(50, 128, 200, 1)),
        (hsla(0, 0, 0, 1.0), hsla(208.8, 0.6, 0.49, 0.9), rgba(0, 0, 0, 1.0)),
        (hsla(0, 0, 0.5, 1.0), hsla(208.8, 0.6, 0.49, 0.5), rgba(128, 128, 128, 1.0)),
        (hsla(0, 0, 1, 1.0), hsla(208.8, 0.6, 0.49, 0.0), rgba(255, 255, 255, 1.0)),
        # Primaries
        (hsla(0, 1, 0.5, 1.0), hsla(120.0, 1, 0.5, 1.0), rgba(255, 0, 0, 1.0)),
        (hsla(120.0, 1, 0.5, 1.0), hsla(0, 1, 0.5, 1.0), rgba(0, 255, 0, 1.0)),
        (hsla(240.0, 1, 0.5, 1.0), hsla(0, 1, 0.5, 1.0), rgba(0, 0, 255, 1.0)),
        # Color with different channel values, including transparency
        (hsla(208.8, 0.6, 0.49, 0.0), hsla(0, 0, 1, 1.0), rgba(255, 255, 255, 1)),
        (hsla(208.8, 0.6, 0.49, 0.5), hsla(0, 0, 0.5, 1.0), rgba(89, 128, 164, 1)),
        (hsla(208.8, 0.6, 0.49, 0.9), hsla(0, 0, 0, 1.0), rgba(45, 115, 180, 1)),
        (hsla(208.8, 0.6, 0.49, 1.0), hsla(0, 0, 0, 0), rgba(50, 128, 200, 1.0)),
        # Both front_color and back_color having intermediate alpha
        (
            hsla(201.29, 1, 0.7, 0.15),
            hsla(321.29, 1, 0.7, 0.85),
            rgba(229, 119, 210, 0.87),
        ),
        (
            hsla(210.0, 0.8, 0.71, 0.2),
            hsla(330.0, 0.8, 0.71, 0.8),
            rgba(212, 136, 195, 0.84),
        ),
        (
            hsla(330.0, 0.5, 0.39, 0.4),
            hsla(90.0, 0.5, 0.39, 0.6),
            rgba(125, 97, 76, 0.76),
        ),
        (
            hsla(210.0, 0.17, 0.24, 0.55),
            hsla(210.0, 0.12, 0.31, 0.45),
            rgba(56, 66, 77, 0.75),
        ),
        (hsla(60.0, 1, 0.5, 0.3), hsla(180.0, 1, 0.5, 0.7), rgba(97, 255, 158, 0.79)),
        #
        # Test with hsl color inputs:
        #
        # Black, gray, white front colors
        (hsl(0, 0, 0), hsl(0, 0, 0), rgba(0, 0, 0, 1.0)),
        (hsl(0, 0, 0), hsl(208.8, 0.6, 0.49), rgba(0, 0, 0, 1.0)),
        (hsl(0, 0, 0.5), hsl(208.8, 0.6, 0.49), rgba(128, 128, 128, 1.0)),
        (hsl(0, 0, 1), hsl(208.8, 0.6, 0.49), rgba(255, 255, 255, 1.0)),
        # Primaries
        (hsl(0, 1, 0.5), hsl(120.0, 1, 0.5), rgba(255, 0, 0, 1.0)),
        (hsl(120.0, 1, 0.5), hsl(0, 1, 0.5), rgba(0, 255, 0, 1.0)),
        (hsl(240.0, 1, 0.5), hsl(0, 1, 0.5), rgba(0, 0, 255, 1.0)),
        # Color with different channel values
        (hsl(208.8, 0.6, 0.49), hsl(0, 0, 1), rgba(50, 128, 200, 1.0)),
        (hsl(208.8, 0.6, 0.49), hsl(0, 0, 0.5), rgba(50, 128, 200, 1.0)),
        (hsl(208.8, 0.6, 0.49), hsl(0, 0, 0), rgba(50, 128, 200, 1.0)),
        # Both front_color and back_color having intermediate values
        (hsl(201.29, 1, 0.7), hsl(321.29, 1, 0.7), rgba(102, 201, 255, 1.0)),
        (hsl(210.0, 0.8, 0.71), hsl(330.0, 0.8, 0.71), rgba(122, 181, 240, 1.0)),
        (hsl(330.0, 0.5, 0.39), hsl(90.0, 0.5, 0.39), rgba(149, 50, 99, 1.0)),
        (hsl(210.0, 0.17, 0.24), hsl(210.0, 0.12, 0.31), rgba(51, 61, 72, 1.0)),
        (hsl(60.0, 1, 0.5), hsl(180.0, 1, 0.5), rgba(255, 255, 0, 1.0)),
        #
        # Test with mixed color class inputs:
        #
        # Black, gray, white front colors
        (rgb(0, 0, 0), rgb(0, 0, 0), rgba(0, 0, 0, 1.0)),
        (hsla(0, 0, 0, 0), rgb(50, 128, 200), rgba(50, 128, 200, 1)),
        (rgb(0, 0, 0), rgb(50, 128, 200), rgba(0, 0, 0, 1.0)),
        (rgba(128, 128, 128, 1.0), rgba(50, 128, 200, 0.5), rgba(128, 128, 128, 1.0)),
        (rgb(255, 255, 255), rgb(50, 128, 200), rgba(255, 255, 255, 1.0)),
        # Primaries
        (hsl(0, 1, 0.5), hsl(120.0, 1, 0.5), rgba(255, 0, 0, 1.0)),
        (rgb(0, 255, 0), hsla(0, 1, 0.5, 1.0), rgba(0, 255, 0, 1.0)),
        (rgb(0, 0, 255), hsla(0, 1, 0.5, 1.0), rgba(0, 0, 255, 1.0)),
        # Color with different channel values, including transparency
        (hsla(208.8, 0.6, 0.49, 0.0), hsla(0, 0, 1, 1.0), rgba(255, 255, 255, 1)),
        (rgba(50, 128, 200, 0.5), hsl(0, 0, 0.5), rgba(89, 128, 164, 1)),
        (hsl(208.8, 0.6, 0.49), rgba(0, 0, 0, 1.0), rgba(50, 128, 200, 1.0)),
        (hsla(208.8, 0.6, 0.49, 1.0), rgba(0, 0, 0, 0), rgba(50, 128, 200, 1.0)),
        # Both front_color and back_color having intermediate values
        (hsla(201.29, 1, 0.7, 0.15), hsl(321.29, 1, 0.7), rgba(232, 117, 209, 1)),
        (hsl(210.0, 0.8, 0.71), hsla(330.0, 0.8, 0.71, 0.8), rgba(122, 181, 240, 1.0)),
        (rgba(150, 50, 100, 0.4), hsla(90.0, 0.5, 0.39, 0.6), rgba(126, 97, 76, 0.76)),
        (rgba(50, 60, 70, 0.55), hsla(210.0, 0.12, 0.31, 0.45), rgba(55, 65, 75, 0.75)),
        (hsla(60.0, 1, 0.5, 0.3), hsla(180.0, 1, 0.5, 0.7), rgba(97, 255, 158, 0.79)),
    ],
)
def test_alpha_blending_over(front_color, back_color, expected_blended_color):
    """The front color can be composited over the back color."""
    # Calculate the blended color using the blend_over() method on the Color class.
    calculated_blended_color = front_color.blend_over(back_color)
    # The calculated blended color will be equal to the expected blended color.
    assert_equal_color(calculated_blended_color, expected_blended_color.rgba, abs=1)


@pytest.mark.parametrize(
    "front_color, back_color",
    [
        # Test with rgba color inputs:
        #
        # Black, gray, white front colors
        (rgba(0, 0, 0, 0), rgba(50, 128, 200, 1.0)),
        (rgba(0, 0, 0, 1.0), rgba(50, 128, 200, 0.9)),
        (rgba(128, 128, 128, 1.0), rgba(50, 128, 200, 0.5)),
        (rgba(255, 255, 255, 1.0), rgba(50, 128, 200, 0.0)),
        # Primaries
        (rgba(255, 0, 0, 1.0), rgba(0, 255, 0, 1.0)),
        (rgba(0, 255, 0, 1.0), rgba(255, 0, 0, 1.0)),
        (rgba(0, 0, 255, 1.0), rgba(255, 0, 0, 1.0)),
        # Color with different channel values, including transparency
        (rgba(50, 128, 200, 0.0), rgba(255, 255, 255, 1.0)),
        (rgba(50, 128, 200, 0.5), rgba(128, 128, 128, 1.0)),
        (rgba(50, 128, 200, 0.9), rgba(0, 0, 0, 1.0)),
        (rgba(50, 128, 200, 1.0), rgba(0, 0, 0, 0)),
        # Both front_color and back_color having intermediate alpha
        (rgba(100, 200, 255, 0.15), rgba(255, 100, 200, 0.85)),
        (rgba(120, 180, 240, 0.2), rgba(240, 120, 180, 0.8)),
        (rgba(150, 50, 100, 0.4), rgba(100, 150, 50, 0.6)),
        (rgba(50, 60, 70, 0.55), rgba(70, 80, 90, 0.45)),
        (rgba(255, 255, 0, 0.3), rgba(0, 255, 255, 0.7)),
        #
        # Test with rgb color inputs:
        #
        # Black, gray, white front colors
        (rgb(0, 0, 0), rgb(50, 128, 200)),
        (rgb(128, 128, 128), rgb(50, 128, 200)),
        (rgb(255, 255, 255), rgb(50, 128, 200)),
        # Primaries
        (rgb(255, 0, 0), rgb(0, 255, 0)),
        (rgb(0, 255, 0), rgb(255, 0, 0)),
        (rgb(0, 0, 255), rgb(255, 0, 0)),
        # Color with different channel values
        (rgb(50, 128, 200), rgb(255, 255, 255)),
        (rgb(50, 128, 200), rgb(128, 128, 128)),
        (rgb(50, 128, 200), rgb(0, 0, 0)),
        # Both front_color and back_color having intermediate values
        (rgb(100, 200, 255), rgb(255, 100, 200)),
        (rgb(120, 180, 240), rgb(240, 120, 180)),
        (rgb(150, 50, 100), rgb(100, 150, 50)),
        (rgb(50, 60, 70), rgb(70, 80, 90)),
        (rgb(255, 255, 0), rgb(0, 255, 255)),
        #
        # Test with hsla color inputs:
        #
        # Black, gray, white front colors
        (hsla(0, 0, 0, 0), hsla(208.8, 0.6, 0.49, 1.0)),
        (hsla(0, 0, 0, 1.0), hsla(208.8, 0.6, 0.49, 0.9)),
        (hsla(0, 0, 0.5, 1.0), hsla(208.8, 0.6, 0.49, 0.5)),
        (hsla(0, 0, 1, 1.0), hsla(208.8, 0.6, 0.49, 0.0)),
        # Primaries
        (hsla(0, 1, 0.5, 1.0), hsla(120.0, 1, 0.5, 1.0)),
        (hsla(120.0, 1, 0.5, 1.0), hsla(0, 1, 0.5, 1.0)),
        (hsla(240.0, 1, 0.5, 1.0), hsla(0, 1, 0.5, 1.0)),
        # Color with different channel values, including transparency
        (hsla(208.8, 0.6, 0.49, 0.0), hsla(0, 0, 1, 1.0)),
        (hsla(208.8, 0.6, 0.49, 0.5), hsla(0, 0, 0.5, 1.0)),
        (hsla(208.8, 0.6, 0.49, 0.9), hsla(0, 0, 0, 1.0)),
        (hsla(208.8, 0.6, 0.49, 1.0), hsla(0, 0, 0, 0)),
        # Both front_color and back_color having intermediate alpha
        (hsla(201.29, 1, 0.7, 0.15), hsla(321.29, 1, 0.7, 0.85)),
        (hsla(210.0, 0.8, 0.71, 0.2), hsla(330.0, 0.8, 0.71, 0.8)),
        (hsla(330.0, 0.5, 0.39, 0.4), hsla(90.0, 0.5, 0.39, 0.6)),
        (hsla(210.0, 0.17, 0.24, 0.55), hsla(210.0, 0.12, 0.31, 0.45)),
        (hsla(60.0, 1, 0.5, 0.3), hsla(180.0, 1, 0.5, 0.7)),
        #
        # Test with hsl color inputs:
        #
        # Black, gray, white front colors
        (hsl(0, 0, 0), hsl(208.8, 0.6, 0.4902)),
        (hsl(0, 0, 0.502), hsl(208.8, 0.6, 0.4902)),
        (hsl(0, 0, 1), hsl(208.8, 0.6, 0.4902)),
        # Primaries
        (hsl(0, 1, 0.5), hsl(120.0, 1, 0.5)),
        (hsl(120.0, 1, 0.5), hsl(0, 1, 0.5)),
        (hsl(240.0, 1, 0.5), hsl(0, 1, 0.5)),
        # Color with different channel values
        (hsl(208.8, 0.6, 0.4902), hsl(0, 0, 1)),
        (hsl(208.8, 0.6, 0.4902), hsl(0, 0, 0.502)),
        (hsl(208.8, 0.6, 0.4902), hsl(0, 0, 0)),
        # Both front_color and back_color having intermediate values
        (hsl(201.2903, 1, 0.6961), hsl(321.2903, 1, 0.6961)),
        (hsl(210.0, 0.8, 0.7059), hsl(330.0, 0.8, 0.7059)),
        (hsl(330.0, 0.5, 0.3922), hsl(90.0, 0.5, 0.3922)),
        (hsl(210.0, 0.1667, 0.2353), hsl(210.0, 0.125, 0.3137)),
        (hsl(60.0, 1, 0.5), hsl(180.0, 1, 0.5)),
        #
        # Test with mixed color class inputs:
        #
        # Black, gray, white front colors
        (hsl(0, 0, 0), hsl(208.8, 0.6, 0.4902)),
        (hsl(0, 0, 0), rgba(50, 128, 200, 0.9)),
        (rgba(128, 128, 128, 1.0), hsla(208.8, 0.6, 0.4902, 0.5)),
        (hsla(0, 0, 1, 1.0), hsl(208.8, 0.6, 0.4902)),
        # Primaries
        (hsl(0, 1, 0.5), rgba(0, 255, 0, 1.0)),
        (hsla(120.0, 1, 0.5, 1.0), hsl(0, 1, 0.5)),
        (rgba(0, 0, 255, 1.0), rgba(255, 0, 0, 1.0)),
        # Color with different channel values, including transparency
        (hsla(208.8, 0.6, 0.4902, 0.0), rgba(255, 255, 255, 1.0)),
        (rgb(50, 128, 200), rgba(128, 128, 128, 1.0)),
        (rgba(50, 128, 200, 0.9), hsl(0, 0, 0)),
        (rgb(50, 128, 200), hsla(0, 0, 0, 0)),
        # Both front_color and back_color having intermediate values
        (hsla(201.2903, 1, 0.6961, 0.15), rgb(255, 100, 200)),
        (hsl(210.0, 0.8, 0.7059), rgb(240, 120, 180)),
        (rgb(150, 50, 100), hsl(90.0, 0.5, 0.3922)),
        (hsla(210.0, 0.1667, 0.2353, 0.55), rgba(70, 80, 90, 0.45)),
        (rgba(255, 255, 0, 0.3), hsla(180.0, 1, 0.5, 0.7)),
    ],
)
def test_alpha_unblend_over(front_color, back_color):
    """The alpha blended color can be unblended to get the original front color."""
    calculated_blended_color = front_color.blend_over(back_color)
    if front_color.a == 0:
        # When the front color has an alpha value of 0, then all information
        # related to the front color will be lost when the color is blended,
        # and the blended color cannot be used to get the original front color.
        with pytest.raises(
            ValueError,
            match=re.escape(
                "The value of front_color_alpha must be within the range of (0, 1]."
            ),
        ):
            calculated_front_color = calculated_blended_color.unblend_over(
                back_color, front_color.a
            )
    else:  # front_color.a != 0:
        # Calculate the original front color from the blended color
        calculated_front_color = calculated_blended_color.unblend_over(
            back_color, front_color.a
        )
        # The derived front color from the blended color, will be equal to the
        # original front color, within the given tolerance range.
        assert_equal_color(calculated_front_color, front_color.rgba, abs=3)
