from toga.colors import rgba


def toga_color(color):
    return rgba(color.R, color.G, color.B, color.A / 255)
