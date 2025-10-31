from PySide6.QtGui import QColor
from travertino.colors import rgb


def native_color(c):
    if c == "transparent":
        return QColor(0, 0, 0, 0)
    return QColor(c.rgba.r, c.rgba.g, c.rgba.b, c.rgba.a * 255)


def toga_color(c):
    if c.alpha() == 0 and c.red() == 0 and c.green() == 0 and c.blue() == 0:
        return "transparent"
    return rgb(c.red(), c.green(), c.blue(), c.alpha() / 255)
