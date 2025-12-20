from android.graphics import Color

from toga.colors import TRANSPARENT

CACHE = {TRANSPARENT: Color.TRANSPARENT}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = Color.argb(int(c.rgb.a * 255), int(c.rgb.r), int(c.rgb.g), int(c.rgb.b))
        CACHE[c] = color

    return color
