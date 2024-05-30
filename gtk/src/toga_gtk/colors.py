COLOR_CACHE = {}


def native_color(c):
    try:
        color = COLOR_CACHE[c]
    except KeyError:
        color = (
            c.rgba.r / 255,
            c.rgba.g / 255,
            c.rgba.b / 255,
            c.rgba.a,
        )
        COLOR_CACHE[c] = color

    return color
