from toga_cocoa.libs import NSColor

CACHE = {}


def native_color(c):
    if not c:
        return None

    try:
        color = CACHE[c]
    except KeyError:
        # Color needs to be retained to be kept in cache.
        color = NSColor.colorWithRed(
            c.rgba.r / 255, green=c.rgba.g / 255, blue=c.rgba.b / 255, alpha=c.rgba.a
        ).retain()
        CACHE[c] = color

    return color
