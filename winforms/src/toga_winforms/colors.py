from System.Drawing import Color
from travertino.colors import TRANSPARENT, rgb, rgba

CACHE = {TRANSPARENT: Color.Transparent}


def native_color_from_toga_color(toga_color):
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


def toga_color_from_native_color(native_color):
    if native_color == Color.Transparent:
        return TRANSPARENT
    else:
        return rgba(
            native_color.R, native_color.G, native_color.B, native_color.A / 255
        )


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
