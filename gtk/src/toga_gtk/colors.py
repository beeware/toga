from toga.colors import rgba

CACHE = {}


def native_color(c):
    try:
        color = CACHE[c]
    except KeyError:
        color = (c.rgba.r / 255, c.rgba.g / 255, c.rgba.b / 255, c.rgba.a)
        CACHE[c] = color

    return color


def parse_color(native_string):
    """Parse a color from a GTK4 native RGB(A) string."""
    if native_string[:4] == "rgba":
        native_string = native_string[4:]
    if native_string[:3] == "rgb":
        native_string = native_string[3:]
    r, g, b, *a = map(float, native_string.strip("()").split(","))
    if a:
        return rgba(r, g, b, a[0])
    else:
        return rgba(r, g, b)
