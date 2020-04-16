from .libs import Color

CACHE = {None: Color.Empty}


def native_color(c):
    color = CACHE.get(c, None)
    if color is not None:
        return color
    color = Color.FromArgb(int(c.rgba.a * 255), c.rgba.r, c.rgba.g, c.rgba.b)
    CACHE[c] = color
    return color
