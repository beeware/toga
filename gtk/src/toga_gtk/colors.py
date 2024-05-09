COLOR_CACHE = {}


def native_color_from_toga_color(toga_color):
    try:
        native_color = COLOR_CACHE[toga_color]
    except KeyError:
        native_color = (
            toga_color.rgba.r / 255,
            toga_color.rgba.g / 255,
            toga_color.rgba.b / 255,
            toga_color.rgba.a,
        )
        COLOR_CACHE[toga_color] = native_color

    return native_color
