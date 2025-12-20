CACHE = {}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = (c.rgb.r / 255, c.rgb.g / 255, c.rgb.b / 255, c.rgb.a)
        CACHE[c] = color

    return color
