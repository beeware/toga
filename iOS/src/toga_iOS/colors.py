from toga.colors import TRANSPARENT
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
