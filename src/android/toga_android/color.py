from android.graphics. import Color


CACHE = {}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = Color.argb(c.rgba.a, c.rgba.r, c.rgba.g, c.rgba.b)
        CACHE[c] = color
    
    return color