import math

from toga.colors import REBECCAPURPLE, WHITE, rgb
from toga.constants import Baseline
from toga.fonts import SANS_SERIF, Font


def fill_head(canvas):
    with canvas.fill(color=rgb(149, 119, 73)):
        canvas.move_to(112, 103)
        canvas.line_to(112, 113)
        canvas.ellipse(73, 114, 39, 47, 0, 0, math.pi)
        canvas.line_to(35, 84)
        canvas.arc(65, 84, 30, math.pi, 3 * math.pi / 2)
        canvas.arc(82, 84, 30, 3 * math.pi / 2, 2 * math.pi)


def stroke_head(canvas):
    with canvas.stroke(line_width=4.0):
        with canvas.close_path():
            canvas.move_to(112, 103)
            canvas.line_to(112, 113)
            canvas.ellipse(73, 114, 39, 47, 0, 0, math.pi)
            canvas.line_to(35, 84)
            canvas.arc(65, 84, 30, math.pi, 3 * math.pi / 2)
            canvas.arc(82, 84, 30, 3 * math.pi / 2, 2 * math.pi)


def draw_eyes(canvas):
    with canvas.fill(color=WHITE):
        canvas.arc(58, 92, 15)
        canvas.arc(88, 92, 15, math.pi, 3 * math.pi)

    # Draw eyes separately to avoid miter join
    with canvas.stroke(line_width=4.0):
        canvas.arc(58, 92, 15)
    with canvas.stroke(line_width=4.0):
        canvas.arc(88, 92, 15, math.pi, 3 * math.pi)

    with canvas.fill():
        canvas.arc(58, 97, 3)
        canvas.arc(88, 97, 3)


def draw_horns(canvas):
    with canvas.stroke(line_width=4.0):
        with canvas.fill(color=rgb(212, 212, 212)):
            canvas.move_to(112, 99)
            canvas.quadratic_curve_to(145, 65, 139, 36)
            canvas.quadratic_curve_to(130, 60, 109, 75)

            canvas.move_to(35, 99)
            canvas.quadratic_curve_to(2, 65, 6, 36)
            canvas.quadratic_curve_to(17, 60, 37, 75)


def draw_nostrils(canvas):
    with canvas.fill(color=rgb(212, 212, 212)):
        canvas.move_to(45, 145)
        canvas.bezier_curve_to(51, 123, 96, 123, 102, 145)
        canvas.ellipse(73, 114, 39, 47, 0, math.pi / 4, 3 * math.pi / 4)
    with canvas.fill():
        canvas.arc(63, 140, 3)
        canvas.arc(83, 140, 3)
    with canvas.stroke(line_width=4.0):
        canvas.move_to(45, 145)
        canvas.bezier_curve_to(51, 123, 96, 123, 102, 145)


def draw_text(canvas):
    font = Font(family=SANS_SERIF, size=20)
    text_width, text_height = canvas.measure_text("Tiberius", font)

    x = (150 - text_width) // 2
    y = 175

    with canvas.stroke(color=REBECCAPURPLE, line_width=4.0):
        canvas.rect(
            x - 5,
            y - 5,
            text_width + 10,
            text_height + 10,
        )
    with canvas.state():
        canvas.fill_style = rgb(149, 119, 73)
        canvas.fill_text("Tiberius", x, y, font=font, baseline=Baseline.TOP)


def draw_tiberius(canvas):
    fill_head(canvas)
    draw_eyes(canvas)
    draw_horns(canvas)
    draw_nostrils(canvas)
    stroke_head(canvas)
    draw_text(canvas)
