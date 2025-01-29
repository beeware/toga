import pytest

from travertino.colors import (
    alpha_blending_over_operation,
    reverse_alpha_blending_over,
    rgba,
)

from ..utils import assert_equal_color


@pytest.mark.parametrize(
    "front_color, back_color",
    [
        # fmt: off
        # Black, gray, white front colors
        (rgba(0, 0, 0, 1.0),        rgba(50, 128, 200, 0.9)),
        (rgba(128, 128, 128, 1.0),  rgba(50, 128, 200, 0.5)),
        # Primaries
        (rgba(255, 0, 0, 1.0),      rgba(0, 255, 0, 1.0)),
        (rgba(0, 255, 0, 1.0),      rgba(255, 0, 0, 1.0)),
        (rgba(0, 0, 255, 1.0),      rgba(255, 0, 0, 1.0)),
        # Color with different channel values, including transparency
        (rgba(50, 128, 200, 0.5),   rgba(128, 128, 128, 1.0)),
        (rgba(50, 128, 200, 0.9),   rgba(0, 0, 0, 1.0)),
        # Both front_color and back_color having intermediate alpha
        (rgba(100, 200, 255, 0.15), rgba(255, 100, 200, 0.85)),
        (rgba(120, 180, 240, 0.2),  rgba(240, 120, 180, 0.8)),
        (rgba(150, 50, 100, 0.4),   rgba(100, 150, 50, 0.6)),
        (rgba(50, 60, 70, 0.55),    rgba(70, 80, 90, 0.45)),
        (rgba(255, 255, 0, 0.3),    rgba(0, 255, 255, 0.7)),
        #
        # The blended color of these cannot be deblended to get the front color.
        # This is because when alpha channel is 0, then the information about
        # the original color will be lost.
        # (rgba(0, 0, 0, 0),          rgba(50, 128, 200, 1.0)),
        # (rgba(255, 255, 255, 1.0),  rgba(50, 128, 200, 0.0)),
        # (rgba(50, 128, 200, 0.0),   rgba(255, 255, 255, 1.0)),
        # (rgba(50, 128, 200, 1.0),   rgba(0, 0, 0, 0)),
        # fmt: on
    ],
)
def test_alpha_blending_over(front_color, back_color):
    calculated_blended_color = alpha_blending_over_operation(front_color, back_color)
    calculated_front_color = reverse_alpha_blending_over(
        calculated_blended_color,
        back_color,
        front_color.a,
    )

    assert_equal_color(calculated_front_color, front_color)
