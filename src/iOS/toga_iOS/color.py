from .libs import UIColor


CACHE = {}


def color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = UIColor.colorWithRed(c.r / 255, green=c.g / 255, blue=c.b / 255, alpha=c.a)

    return color
