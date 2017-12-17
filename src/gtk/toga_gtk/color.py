CACHE = {}


def color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = (c.r / 255, c.g / 255, c.b / 255, c.a)

    return color
