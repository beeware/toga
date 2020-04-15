from .libs import Color

CACHE = {None: Color.Empty}


def native_color(c):
    if c in CACHE:
        return CACHE[c]
    color = Color.FromArgb(int(c.rgba.a * 255), c.rgba.r, c.rgba.g, c.rgba.b)
    CACHE[c] = color
    return color
