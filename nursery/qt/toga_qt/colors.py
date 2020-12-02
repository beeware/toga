# Use the Travertino color definitions
from travertino.colors import *  # noqa: F401,F403
from PySide2.QtGui import QColor


def native_color(c):
    if isinstance(c, str):
        c = NAMED_COLOR[c]

    return QColor.fromRgb(c.rgba.r, c.rgba.g, c.rgba.b, c.rgba.a * 255)
