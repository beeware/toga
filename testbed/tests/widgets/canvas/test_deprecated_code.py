import math

import pytest

import toga
from toga.colors import WHITE, rgb
from toga.constants import SANS_SERIF, Baseline

from .test_canvas import assert_reference


async def test_old_tutorial(canvas, probe):
    """The previous code in tutorial 4 still renders correctly."""

    # Shift the whole thing up a bit so we can see all of it.
    canvas.translate(0, -20)

    with pytest.deprecated_call():
        # Fill head

        with canvas.Fill(color=rgb(149, 119, 73)) as head_filler:
            head_filler.move_to(112, 103)
            head_filler.line_to(112, 113)
            head_filler.ellipse(73, 114, 39, 47, 0, 0, math.pi)
            head_filler.line_to(35, 84)
            head_filler.arc(65, 84, 30, math.pi, 3 * math.pi / 2)
            head_filler.arc(82, 84, 30, 3 * math.pi / 2, 2 * math.pi)

        # Eyes

        with canvas.Fill(color=WHITE) as eye_whites:
            eye_whites.arc(58, 92, 15)
            eye_whites.arc(88, 92, 15, math.pi, 3 * math.pi)

        # Draw eyes separately to avoid miter join
        with canvas.Stroke(line_width=4.0) as eye_outline:
            eye_outline.arc(58, 92, 15)
        with canvas.Stroke(line_width=4.0) as eye_outline:
            eye_outline.arc(88, 92, 15, math.pi, 3 * math.pi)

        with canvas.Fill() as eye_pupils:
            eye_pupils.arc(58, 97, 3)
            eye_pupils.arc(88, 97, 3)

        # Horns

        with canvas.root_state.state() as r_horn:
            with r_horn.Fill(color=rgb(212, 212, 212)) as r_horn_filler:
                r_horn_filler.move_to(112, 99)
                r_horn_filler.quadratic_curve_to(145, 65, 139, 36)
                r_horn_filler.quadratic_curve_to(130, 60, 109, 75)
            with r_horn.Stroke(line_width=4.0) as r_horn_stroker:
                r_horn_stroker.move_to(112, 99)
                r_horn_stroker.quadratic_curve_to(145, 65, 139, 36)
                r_horn_stroker.quadratic_curve_to(130, 60, 109, 75)

        with canvas.root_state.state() as l_horn:
            with l_horn.Fill(color=rgb(212, 212, 212)) as l_horn_filler:
                l_horn_filler.move_to(35, 99)
                l_horn_filler.quadratic_curve_to(2, 65, 6, 36)
                l_horn_filler.quadratic_curve_to(17, 60, 37, 75)
            with l_horn.Stroke(line_width=4.0) as l_horn_stroker:
                l_horn_stroker.move_to(35, 99)
                l_horn_stroker.quadratic_curve_to(2, 65, 6, 36)
                l_horn_stroker.quadratic_curve_to(17, 60, 37, 75)

        # Nostrils

        with canvas.Fill(color=rgb(212, 212, 212)) as nose_filler:
            nose_filler.move_to(45, 145)
            nose_filler.bezier_curve_to(51, 123, 96, 123, 102, 145)
            nose_filler.ellipse(73, 114, 39, 47, 0, math.pi / 4, 3 * math.pi / 4)
        with canvas.Fill() as nostril_filler:
            nostril_filler.arc(63, 140, 3)
            nostril_filler.arc(83, 140, 3)
        with canvas.Stroke(line_width=4.0) as nose_stroker:
            nose_stroker.move_to(45, 145)
            nose_stroker.bezier_curve_to(51, 123, 96, 123, 102, 145)

        # Outline head

        with canvas.Stroke(line_width=4.0) as head_outline:
            with head_outline.ClosedPath(112, 103) as closed_head:
                closed_head.line_to(112, 113)
                closed_head.ellipse(73, 114, 39, 47, 0, 0, math.pi)
                closed_head.line_to(35, 84)
                closed_head.arc(65, 84, 30, math.pi, 3 * math.pi / 2)
                closed_head.arc(82, 84, 30, 3 * math.pi / 2, 2 * math.pi)

        # Text

        font = toga.Font(family=SANS_SERIF, size=20)
        text_width, text_height = canvas.measure_text("Tiberius", font)

        x = (150 - text_width) // 2
        y = 175

        with canvas.Stroke(color="REBECCAPURPLE", line_width=4.0) as rect_stroker:
            text_border = rect_stroker.rect(  # noqa: F841
                x - 5,
                y - 5,
                text_width + 10,
                text_height + 10,
            )
        with canvas.Fill(color=rgb(149, 119, 73)) as text_filler:
            text = text_filler.write_text("Tiberius", x, y, font, Baseline.TOP)  # noqa: F841

    await probe.redraw("Tiberus should be drawn")
    assert_reference(probe, "deprecated_tutorial")
