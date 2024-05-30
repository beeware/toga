from System.Drawing import Color
from travertino.colors import TRANSPARENT, rgb, rgba

CACHE = {TRANSPARENT: Color.Transparent}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = Color.FromArgb(
            int(c.rgba.a * 255),
            int(c.rgba.r),
            int(c.rgba.g),
            int(c.rgba.b),
        )
        CACHE[c] = color

    return color


def toga_color(c):
    if c == Color.Transparent:
        return TRANSPARENT
    else:
        return rgba(c.R, c.G, c.B, c.A / 255)


def alpha_blending_over_operation(front_color, back_color):
    # The blending operation implemented here is the "over" operation and
    # replicates CSS's rgba mechanism. For the formula used here, see:
    # https://en.wikipedia.org/wiki/Alpha_compositing#Description

    blended_alpha = min(
        1, max(0, (front_color.a + ((1 - front_color.a) * back_color.a)))
    )

    blended_color = rgb(
        # Red Component
        min(
            255,
            max(
                0,
                round(
                    (
                        (front_color.r * front_color.a)
                        + (back_color.r * back_color.a * (1 - front_color.a))
                    )
                    / blended_alpha
                ),
            ),
        ),
        # Green Component
        min(
            255,
            max(
                0,
                round(
                    (
                        (front_color.g * front_color.a)
                        + (back_color.g * back_color.a * (1 - front_color.a))
                    )
                    / blended_alpha
                ),
            ),
        ),
        # Blue Component
        min(
            255,
            max(
                0,
                round(
                    (
                        (front_color.b * front_color.a)
                        + (back_color.b * back_color.a * (1 - front_color.a))
                    )
                    / blended_alpha
                ),
            ),
        ),
    )
    return blended_color
