from android.graphics import Color
from travertino.colors import TRANSPARENT

CACHE = {TRANSPARENT: Color.TRANSPARENT}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = Color.argb(
            int(c.rgba.a * 255), int(c.rgba.r), int(c.rgba.g), int(c.rgba.b)
        )
        CACHE[c] = color

    return color
