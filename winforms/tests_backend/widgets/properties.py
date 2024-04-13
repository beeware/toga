from System.Drawing import ContentAlignment
from System.Windows.Forms import HorizontalAlignment

from toga.colors import rgba
from toga.style.pack import BOTTOM, CENTER, LEFT, RIGHT, TOP


def toga_color(color):
    return rgba(color.R, color.G, color.B, color.A / 255)


def reverse_alpha_blending_over_operation(blended_color, parent_color, child_alpha):
    # This is the reverse of the "over" operation. I have derived
    # this formula from the "over" operation formula, see:
    # https://en.wikipedia.org/wiki/Alpha_compositing#Description

    child_color = rgba(
        round(
            (
                (blended_color.r * blended_color.a)
                - (parent_color.r * parent_color.a * (1 - child_alpha))
            )
            / child_alpha
        ),
        round(
            (
                (blended_color.g * blended_color.a)
                - (parent_color.g * parent_color.a * (1 - child_alpha))
            )
            / child_alpha
        ),
        round(
            (
                (blended_color.b * blended_color.a)
                - (parent_color.b * parent_color.a * (1 - child_alpha))
            )
            / child_alpha
        ),
        child_alpha,
    )
    return child_color


def toga_xalignment(alignment):
    return {
        ContentAlignment.TopLeft: LEFT,
        ContentAlignment.MiddleLeft: LEFT,
        ContentAlignment.BottomLeft: LEFT,
        ContentAlignment.TopCenter: CENTER,
        ContentAlignment.MiddleCenter: CENTER,
        ContentAlignment.BottomCenter: CENTER,
        ContentAlignment.TopRight: RIGHT,
        ContentAlignment.MiddleRight: RIGHT,
        ContentAlignment.BottomRight: RIGHT,
        #
        HorizontalAlignment.Left: LEFT,
        HorizontalAlignment.Center: CENTER,
        HorizontalAlignment.Right: RIGHT,
    }[alignment]


def toga_yalignment(alignment):
    return {
        ContentAlignment.TopLeft: TOP,
        ContentAlignment.TopCenter: TOP,
        ContentAlignment.TopRight: TOP,
        ContentAlignment.MiddleLeft: CENTER,
        ContentAlignment.MiddleCenter: CENTER,
        ContentAlignment.MiddleRight: CENTER,
        ContentAlignment.BottomLeft: BOTTOM,
        ContentAlignment.BottomCenter: BOTTOM,
        ContentAlignment.BottomRight: BOTTOM,
    }[alignment]
