from gi.repository import Gdk

CACHE = {}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = Gdk.RGBA()
        color.red = c.rgba.r/255
        color.green = c.rgba.g/255
        color.blue = c.rgba.b/255
        color.alpha = c.rgba.a

    return color
