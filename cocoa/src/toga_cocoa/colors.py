from toga_cocoa.libs import NSColor

COLOR_CACHE = {}


def native_color(c):
    if not c:
        return None

    try:
        color = COLOR_CACHE[c]
    except KeyError:
        # Color needs to be retained to be kept in cache.
        color = NSColor.colorWithRed(
            c.rgba.r / 255, green=c.rgba.g / 255, blue=c.rgba.b / 255, alpha=c.rgba.a
        ).retain()
        COLOR_CACHE[c] = color

    return color
