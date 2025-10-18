import re

import pytest

from travertino.colors import hsl, rgb

from ..utils import assert_equal_color

front_back_blended = pytest.mark.parametrize(
    "front_color, back_color, expected_blended_color",
    [
        # Test with rgb color inputs:
        #
        # Black, gray, white front colors...
        (rgb(0, 0, 0), rgb(0, 0, 0), rgb(0, 0, 0)),
        (rgb(0, 0, 0), rgb(50, 128, 200, 0.9), rgb(0, 0, 0)),
        (rgb(128, 128, 128), rgb(50, 128, 200, 0.5), rgb(128, 128, 128)),
        (rgb(255, 255, 255), rgb(50, 128, 200, 0.0), rgb(255, 255, 255)),
        # ...plus transparency
        (rgb(0, 0, 0, 0), rgb(0, 0, 0, 0), rgb(0, 0, 0, 0)),
        (rgb(0, 0, 0, 0), rgb(50, 128, 200), rgb(50, 128, 200)),
        # Opaque primaries
        (rgb(255, 0, 0), rgb(0, 255, 0), rgb(255, 0, 0)),
        (rgb(0, 255, 0), rgb(255, 0, 0), rgb(0, 255, 0)),
        (rgb(0, 0, 255), rgb(255, 0, 0), rgb(0, 0, 255)),
        # Color with different channel values...
        (rgb(50, 128, 200), rgb(255, 255, 255), rgb(50, 128, 200)),
        (rgb(50, 128, 200), rgb(128, 128, 128), rgb(50, 128, 200)),
        (rgb(50, 128, 200), rgb(0, 0, 0), rgb(50, 128, 200)),
        # ...plus transparency
        (rgb(50, 128, 200, 0.0), rgb(255, 255, 255, 1.0), rgb(255, 255, 255)),
        (rgb(50, 128, 200, 0.5), rgb(128, 128, 128, 1.0), rgb(89, 128, 164)),
        (rgb(50, 128, 200, 0.9), rgb(0, 0, 0, 1.0), rgb(45, 115, 180)),
        (rgb(50, 128, 200, 1.0), rgb(0, 0, 0, 0), rgb(50, 128, 200)),
        # Both front_color and back_color having intermediate values...
        (rgb(100, 200, 255), rgb(255, 100, 200), rgb(100, 200, 255)),
        (rgb(120, 180, 240), rgb(240, 120, 180), rgb(120, 180, 240)),
        (rgb(150, 50, 100), rgb(100, 150, 50), rgb(150, 50, 100)),
        (rgb(50, 60, 70), rgb(70, 80, 90), rgb(50, 60, 70)),
        (rgb(255, 255, 0), rgb(0, 255, 255), rgb(255, 255, 0)),
        # ...and intermediate alpha too
        (
            rgb(100, 200, 255, 0.15),
            rgb(255, 100, 200, 0.85),
            rgb(228, 117, 209, 0.87),
        ),
        (rgb(120, 180, 240, 0.2), rgb(240, 120, 180, 0.8), rgb(211, 134, 194, 0.84)),
        (rgb(150, 50, 100, 0.4), rgb(100, 150, 50, 0.6), rgb(126, 97, 76, 0.76)),
        (rgb(50, 60, 70, 0.55), rgb(70, 80, 90, 0.45), rgb(55, 65, 75, 0.75)),
        (rgb(255, 255, 0, 0.3), rgb(0, 255, 255, 0.7), rgb(97, 255, 158, 0.79)),
        #
        # Test with hsl color inputs:
        #
        # Black, gray, white front colors...
        (hsl(0, 0, 0), hsl(0, 0, 0), rgb(0, 0, 0, 1.0)),
        (hsl(0, 0, 0), hsl(208.8, 0.6, 0.49), rgb(0, 0, 0, 1.0)),
        (hsl(0, 0, 0.5), hsl(208.8, 0.6, 0.49), rgb(128, 128, 128, 1.0)),
        (hsl(0, 0, 1), hsl(208.8, 0.6, 0.49), rgb(255, 255, 255, 1.0)),
        # ...plus transparency
        (hsl(0, 0, 0, 0), hsl(0, 0, 0, 0), rgb(0, 0, 0, 0)),
        (hsl(0, 0, 0, 0), hsl(208.8, 0.6, 0.49, 1.0), rgb(50, 128, 200, 1)),
        (hsl(0, 0, 0, 1.0), hsl(208.8, 0.6, 0.49, 0.9), rgb(0, 0, 0, 1.0)),
        (hsl(0, 0, 0.5, 1.0), hsl(208.8, 0.6, 0.49, 0.5), rgb(128, 128, 128, 1.0)),
        (hsl(0, 0, 1, 1.0), hsl(208.8, 0.6, 0.49, 0.0), rgb(255, 255, 255, 1.0)),
        # Opaque primaries
        (hsl(0, 1, 0.5), hsl(120.0, 1, 0.5), rgb(255, 0, 0)),
        (hsl(120.0, 1, 0.5), hsl(0, 1, 0.5), rgb(0, 255, 0)),
        (hsl(240.0, 1, 0.5), hsl(0, 1, 0.5), rgb(0, 0, 255)),
        # Transparent primaries
        (hsl(0, 1, 0.5), hsl(120.0, 1, 0.5), rgb(255, 0, 0)),
        (hsl(120.0, 1, 0.5), hsl(0, 1, 0.5), rgb(0, 255, 0)),
        (hsl(240.0, 1, 0.5), hsl(0, 1, 0.5), rgb(0, 0, 255)),
        # Color with different channel values...
        (hsl(208.8, 0.6, 0.49), hsl(0, 0, 1), rgb(50, 128, 200, 1.0)),
        (hsl(208.8, 0.6, 0.49), hsl(0, 0, 0.5), rgb(50, 128, 200, 1.0)),
        (hsl(208.8, 0.6, 0.49), hsl(0, 0, 0), rgb(50, 128, 200, 1.0)),
        # ...plus transparency
        (hsl(208.8, 0.6, 0.49, 0.0), hsl(0, 0, 1, 1.0), rgb(255, 255, 255, 1)),
        (rgb(50, 128, 200, 0.5), hsl(0, 0, 0.5), rgb(89, 128, 164, 1)),
        (hsl(208.8, 0.6, 0.49), rgb(0, 0, 0, 1.0), rgb(50, 128, 200, 1.0)),
        (hsl(208.8, 0.6, 0.49, 1.0), rgb(0, 0, 0, 0), rgb(50, 128, 200, 1.0)),
        # Both front_color and back_color having intermediate values...
        (hsl(201.29, 1, 0.7), hsl(321.29, 1, 0.7), rgb(102, 201, 255, 1.0)),
        (hsl(210.0, 0.8, 0.71), hsl(330.0, 0.8, 0.71), rgb(122, 181, 240, 1.0)),
        (hsl(330.0, 0.5, 0.39), hsl(90.0, 0.5, 0.39), rgb(149, 50, 99, 1.0)),
        (hsl(210.0, 0.17, 0.24), hsl(210.0, 0.12, 0.31), rgb(51, 61, 72, 1.0)),
        (hsl(60.0, 1, 0.5), hsl(180.0, 1, 0.5), rgb(255, 255, 0, 1.0)),
        # ...and intermediate alpha too
        (
            hsl(201.29, 1, 0.7, 0.15),
            hsl(321.29, 1, 0.7, 0.85),
            rgb(229, 119, 210, 0.87),
        ),
        (
            hsl(210.0, 0.8, 0.71, 0.2),
            hsl(330.0, 0.8, 0.71, 0.8),
            rgb(212, 136, 195, 0.84),
        ),
        (
            hsl(330.0, 0.5, 0.39, 0.4),
            hsl(90.0, 0.5, 0.39, 0.6),
            rgb(125, 97, 76, 0.76),
        ),
        (
            hsl(210.0, 0.17, 0.24, 0.55),
            hsl(210.0, 0.12, 0.31, 0.45),
            rgb(56, 66, 77, 0.75),
        ),
        (hsl(60.0, 1, 0.5, 0.3), hsl(180.0, 1, 0.5, 0.7), rgb(97, 255, 158, 0.79)),
        # Test with mixed color class inputs:
        #
        # Black, gray, white front colors
        (hsl(0, 0, 0, 0), rgb(50, 128, 200), rgb(50, 128, 200, 1)),
        # Primaries
        (rgb(0, 255, 0), hsl(0, 1, 0.5, 1.0), rgb(0, 255, 0, 1.0)),
        (rgb(0, 0, 255), hsl(0, 1, 0.5, 1.0), rgb(0, 0, 255, 1.0)),
        # Color with different channel values, including transparency
        (rgb(50, 128, 200, 0.5), hsl(0, 0, 0.5), rgb(89, 128, 164, 1)),
        (hsl(208.8, 0.6, 0.49), rgb(0, 0, 0, 1.0), rgb(50, 128, 200, 1.0)),
        (hsl(208.8, 0.6, 0.49, 1.0), rgb(0, 0, 0, 0), rgb(50, 128, 200, 1.0)),
        # Both front_color and back_color having intermediate values
        (rgb(150, 50, 100, 0.4), hsl(90.0, 0.5, 0.39, 0.6), rgb(126, 97, 76, 0.76)),
        (rgb(50, 60, 70, 0.55), hsl(210.0, 0.12, 0.31, 0.45), rgb(55, 65, 75, 0.75)),
    ],
)


@front_back_blended
def test_alpha_blending_over(front_color, back_color, expected_blended_color):
    """The front color can be composited over the back color."""
    # Calculate the blended color using the blend_over() method on the Color class.
    calculated_blended_color = front_color.blend_over(back_color)
    # The calculated blended color will be equal to the expected blended color.
    assert_equal_color(calculated_blended_color, expected_blended_color.rgb, abs=1)


@front_back_blended
def test_alpha_unblend_over(front_color, back_color, expected_blended_color):
    """The alpha blended color can be unblended to get the original front color."""
    _ = expected_blended_color  # Not used for this test

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
        assert_equal_color(calculated_front_color, front_color.rgb, abs=3)
