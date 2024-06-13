from ctypes import byref

from rubicon.objc import CGFloat

from toga.colors import TRANSPARENT, rgba
from toga_iOS.libs import UIColor

CACHE = {TRANSPARENT: UIColor.clearColor}


def native_color(c):
    if not c:
        return None

    try:
        color = CACHE[c]
    except KeyError:
        # Color needs to be retained to be kept in the cache
        color = UIColor.colorWithRed(
            c.rgba.r / 255, green=c.rgba.g / 255, blue=c.rgba.b / 255, alpha=c.rgba.a
        ).retain()
        CACHE[c] = color

    return color


def toga_color(c):
    if c == UIColor.clearColor:
        return TRANSPARENT

    red = CGFloat()
    green = CGFloat()
    blue = CGFloat()
    alpha = CGFloat()
    c.getRed(byref(red), green=byref(green), blue=byref(blue), alpha=byref(alpha))
    return rgba(red.value * 255, green.value * 255, blue.value * 255, alpha.value)
