import re

import pytest

from travertino.colors import (
    reverse_straight_alpha_blending_over,
    rgba,
    straight_alpha_blending_over,
)

from ..utils import assert_equal_color


@pytest.mark.parametrize(
    "front_color, back_color, expected_blended_color",
    [
        # Black, gray, white front colors
        (rgba(0, 0, 0, 0), rgba(0, 0, 0, 0), rgba(0, 0, 0, 0)),
        (rgba(0, 0, 0, 0), rgba(50, 128, 200, 1.0), rgba(50, 128, 200, 1.0)),
        (rgba(0, 0, 0, 1.0), rgba(50, 128, 200, 0.9), rgba(0, 0, 0, 1.0)),
        (rgba(128, 128, 128, 1.0), rgba(50, 128, 200, 0.5), rgba(128, 128, 128, 1.0)),
        (rgba(255, 255, 255, 1.0), rgba(50, 128, 200, 0.0), rgba(255, 255, 255, 1.0)),
        # Primaries
        (rgba(255, 0, 0, 1.0), rgba(0, 255, 0, 1.0), rgba(255, 0, 0, 1.0)),
        (rgba(0, 255, 0, 1.0), rgba(255, 0, 0, 1.0), rgba(0, 255, 0, 1.0)),
        (rgba(0, 0, 255, 1.0), rgba(255, 0, 0, 1.0), rgba(0, 0, 255, 1.0)),
        # Color with different channel values, including transparency
        (rgba(50, 128, 200, 0.0), rgba(255, 255, 255, 1.0), rgba(255, 255, 255, 1.0)),
        (rgba(50, 128, 200, 0.5), rgba(128, 128, 128, 1.0), rgba(89, 128, 164, 1)),
        (rgba(50, 128, 200, 0.9), rgba(0, 0, 0, 1.0), rgba(45, 115, 180, 1)),
        (rgba(50, 128, 200, 1.0), rgba(0, 0, 0, 0), rgba(50, 128, 200, 1)),
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
    ],
)
def test_alpha_blending_over(front_color, back_color, expected_blended_color):
    """The front color can be composited over the back color."""
    # Calculate the blended color using the function directly:
    calculated_blended_color1 = straight_alpha_blending_over(front_color, back_color)
    # The calculated blended color will be equal to the expected blended color.
    assert_equal_color(calculated_blended_color1, expected_blended_color)

    # Calculate the blended color using the blend_over() method on the Color class:
    calculated_blended_color2 = front_color.blend_over(back_color)
    # The calculated blended color will be equal to the expected blended color.
    assert_equal_color(calculated_blended_color2, expected_blended_color)


@pytest.mark.parametrize(
    "front_color, back_color",
    [
        # fmt: off
        # Black, gray, white front colors
        (rgba(0, 0, 0, 1.0),        rgba(50, 128, 200, 0.9)),
        (rgba(128, 128, 128, 1.0),  rgba(50, 128, 200, 0.5)),
        (rgba(255, 255, 255, 1.0),  rgba(50, 128, 200, 0.0)),
        # Primaries
        (rgba(255, 0, 0, 1.0),      rgba(0, 255, 0, 1.0)),
        (rgba(0, 255, 0, 1.0),      rgba(255, 0, 0, 1.0)),
        (rgba(0, 0, 255, 1.0),      rgba(255, 0, 0, 1.0)),
        # Color with different channel values, including transparency
        (rgba(50, 128, 200, 0.5),   rgba(128, 128, 128, 1.0)),
        (rgba(50, 128, 200, 0.9),   rgba(0, 0, 0, 1.0)),
        (rgba(50, 128, 200, 1.0),   rgba(0, 0, 0, 0)),
        # Both front_color and back_color having intermediate alpha
        (rgba(100, 200, 255, 0.15), rgba(255, 100, 200, 0.85)),
        (rgba(120, 180, 240, 0.2),  rgba(240, 120, 180, 0.8)),
        (rgba(150, 50, 100, 0.4),   rgba(100, 150, 50, 0.6)),
        (rgba(50, 60, 70, 0.55),    rgba(70, 80, 90, 0.45)),
        (rgba(255, 255, 0, 0.3),    rgba(0, 255, 255, 0.7)),
        #
        # The blended color of these pairs, cannot be deblended to get the front
        # color. This is because when alpha channel of the front color is 0, then
        # the blended color will be equal to the back color. Therefore, all of the
        # information about the original front color will be lost.
        (rgba(0, 0, 0, 0),          rgba(50, 128, 200, 1.0)),
        (rgba(50, 128, 200, 0.0),   rgba(255, 255, 255, 1.0)),
        # fmt: on
    ],
)
def test_reverse_straight_alpha_blending_over(front_color, back_color):
    """The alpha blended color can be unblended to get the original front color."""
    # Calculate the alpha blended color, keep the decimal precision, as the
    # blended color will be deblended to get the original front color.
    calculated_blended_color = straight_alpha_blending_over(
        front_color, back_color, round_to_nearest_int=False
    )
    if front_color.a == 0:
        # When the front color has an alpha value of 0, then all information
        # related to the front color will be lost, and the blended color
        # cannot be deblended to get the original front color.
        with pytest.raises(
            ValueError,
            match=re.escape(
                "The value of front_color_alpha must be within the range of (0, 1]."
            ),
        ):
            calculated_front_color = reverse_straight_alpha_blending_over(
                calculated_blended_color, back_color, front_color.a
            )
    else:  # front_color.a != 0:
        # Calculate the original front color from the blended color
        calculated_front_color = reverse_straight_alpha_blending_over(
            calculated_blended_color, back_color, front_color.a
        )
        # The derived front color from the blended color, will be equal to the
        # original front color, within the given tolerance range.
        assert_equal_color(calculated_front_color, front_color)
