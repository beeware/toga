from toga_iOS.libs import UIColor

CACHE = {}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = UIColor.colorWithRed(c.rgba.r / 255, green=c.rgba.g / 255, blue=c.rgba.b / 255, alpha=c.rgba.a)
        CACHE[c] = color

    return color
