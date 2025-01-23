CACHE = {}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = (c.rgba.r / 255, c.rgba.g / 255, c.rgba.b / 255, c.rgba.a)

    return color
