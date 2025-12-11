from System.Drawing import Color

from toga.colors import TRANSPARENT, rgb

CACHE = {TRANSPARENT: Color.Transparent}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = Color.FromArgb(
            int(c.rgb.a * 255),
            int(c.rgb.r),
            int(c.rgb.g),
            int(c.rgb.b),
        )
        CACHE[c] = color

    return color


def toga_color(c):
    return rgb(c.R, c.G, c.B, c.A / 255)
