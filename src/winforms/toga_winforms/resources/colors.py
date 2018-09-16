from .libs import Color

CACHE = {}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = Color.FromArgb(int(c.rgba.a * 255), c.rgba.r, c.rgba.g, c.rgba.b)
        CACHE[c] = color
    return color
