from System.Drawing import ContentAlignment
from System.Windows.Forms import HorizontalAlignment

from toga.colors import rgba
from toga.style.pack import BOTTOM, CENTER, LEFT, RIGHT, TOP


def toga_color(color):
    return rgba(color.R, color.G, color.B, color.A / 255)


def toga_xalignment(alignment):
    return {
        ContentAlignment.TopLeft: LEFT,
        ContentAlignment.MiddleLeft: LEFT,
        ContentAlignment.BottomLeft: LEFT,
        ContentAlignment.TopCenter: CENTER,
        ContentAlignment.MiddleCenter: CENTER,
        ContentAlignment.BottomCenter: CENTER,
        ContentAlignment.TopRight: RIGHT,
        ContentAlignment.MiddleRight: RIGHT,
        ContentAlignment.BottomRight: RIGHT,
        #
        HorizontalAlignment.Left: LEFT,
        HorizontalAlignment.Center: CENTER,
        HorizontalAlignment.Right: RIGHT,
    }[alignment]


def toga_yalignment(alignment):
    return {
        ContentAlignment.TopLeft: TOP,
        ContentAlignment.TopCenter: TOP,
        ContentAlignment.TopRight: TOP,
        ContentAlignment.MiddleLeft: CENTER,
        ContentAlignment.MiddleCenter: CENTER,
        ContentAlignment.MiddleRight: CENTER,
        ContentAlignment.BottomLeft: BOTTOM,
        ContentAlignment.BottomCenter: BOTTOM,
        ContentAlignment.BottomRight: BOTTOM,
    }[alignment]
