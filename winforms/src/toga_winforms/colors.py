from System.Drawing import Color
from travertino.colors import NAMED_COLOR, TRANSPARENT

CACHE = {TRANSPARENT: Color.Transparent}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        if isinstance(c, str):
            c = NAMED_COLOR[c]
        color = Color.FromArgb(
            int(c.rgba.a * 255), int(c.rgba.r), int(c.rgba.g), int(c.rgba.b)
        )
        CACHE[c] = color

    return color
