from toga.colors import TRANSPARENT
from toga_iOS.libs import UIColor

CACHE = {TRANSPARENT: UIColor.clearColor}


def native_color(c):
    if not c:
        return None

    try:
        color = CACHE[c]
    except KeyError:
        color = UIColor.colorWithRed(
            c.rgb.r / 255, green=c.rgb.g / 255, blue=c.rgb.b / 255, alpha=c.rgb.a
        )
        CACHE[c] = color

    return color
