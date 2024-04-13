from System.Drawing import Color
from travertino.colors import TRANSPARENT, rgb, rgba

CACHE = {TRANSPARENT: Color.Transparent}


def native_color(toga_color):
    try:
        color = CACHE[toga_color]
    except KeyError:
        color = Color.FromArgb(
            int(toga_color.rgba.a * 255),
            int(toga_color.rgba.r),
            int(toga_color.rgba.g),
            int(toga_color.rgba.b),
        )
        CACHE[toga_color] = color

    return color


def toga_color(native_color):
    return rgba(native_color.R, native_color.G, native_color.B, native_color.A / 255)


def alpha_blending_over_operation(child_color, parent_color):
    # The blending operation I have implemented here is the "over" operation and
    # replicates CSS's rgba mechanism. For the formula used here, see:
    # https://en.wikipedia.org/wiki/Alpha_compositing#Description

    blended_alpha = child_color.a + ((1 - child_color.a) * parent_color.a)

    # Check if the blended alpha is zero, indicating no blending
    if blended_alpha == 0:
        # If both child and parent alphas are 0, no blending occurs, so return child color.
        return child_color

    blended_color = rgb(
        # Red Component
        (
            (
                (child_color.r * child_color.a)
                + (parent_color.r * parent_color.a * (1 - child_color.a))
            )
            / blended_alpha
        ),
        # Green Component
        (
            (
                (child_color.g * child_color.a)
                + (parent_color.g * parent_color.a * (1 - child_color.a))
            )
            / blended_alpha
        ),
        # Blue Component
        (
            (
                (child_color.b * child_color.a)
                + (parent_color.b * parent_color.a * (1 - child_color.a))
            )
            / blended_alpha
        ),
    )
    return blended_color
