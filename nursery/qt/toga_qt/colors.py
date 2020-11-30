# Use the Travertino color definitions
from travertino.colors import *  # noqa: F401,F403
from toga_qt.libs import QtGui


def native_color(c):
    if isinstance(c, str):
        c = NAMED_COLOR[c]

    return QtGui.QColor.fromRgb(c.rgba.r, c.rgba.g, c.rgba.b, c.rgba.a * 255)
