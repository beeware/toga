from travertino.colors import NAMED_COLOR, TRANSPARENT

from .libs.android.graphics import Color

CACHE = {
    TRANSPARENT: Color.TRANSPARENT
}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        if isinstance(c, str):
            c = NAMED_COLOR[c]
        color = Color.argb(
            int(c.rgba.a * 255),
            int(c.rgba.r),
            int(c.rgba.g),
            int(c.rgba.b)
        )
        CACHE[c] = color

    return color
