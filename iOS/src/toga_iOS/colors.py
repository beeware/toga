from toga.colors import TRANSPARENT
from toga_iOS.libs import UIColor

COLOR_CACHE = {TRANSPARENT: UIColor.clearColor}


def native_color_from_toga_color(toga_color):
    if not toga_color:
        return None

    try:
        native_color = COLOR_CACHE[toga_color]
    except KeyError:
        # Color needs to be retained to be kept in the cache
        native_color = UIColor.colorWithRed(
            toga_color.rgba.r / 255,
            green=toga_color.rgba.g / 255,
            blue=toga_color.rgba.b / 255,
            alpha=toga_color.rgba.a,
        ).retain()
        COLOR_CACHE[toga_color] = native_color

    return native_color
