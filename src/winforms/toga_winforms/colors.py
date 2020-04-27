from travertino.colors import NAMED_COLOR

from .libs import Color

CACHE = {None: Color.Empty}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        if isinstance(c, str):
            c = NAMED_COLOR[c]
        color = Color.FromArgb(int(c.rgba.a * 255), c.rgba.r, c.rgba.g, c.rgba.b)
        CACHE[c] = color

    return color
