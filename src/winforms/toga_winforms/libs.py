import clr
clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms
from System import Decimal as ClrDecimal
from System import Convert
from System import Threading
from System import Uri
from System.Drawing import Size, Point, Color, ContentAlignment, Bitmap
from System.Drawing import Icon as WinIcon
from System.Drawing import Image as WinImage

from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY

def TextAlignment(value):
    return {
        LEFT: ContentAlignment.MiddleLeft,
        RIGHT: ContentAlignment.MiddleRight,
        CENTER: ContentAlignment.MiddleCenter,
        JUSTIFY: ContentAlignment.MiddleLeft,
    }[value]


# Justify simply sets Left alignment. Is this the best option?
def HorizontalTextAlignment(value):
    return {
        LEFT: WinForms.HorizontalAlignment.Left,
        RIGHT: WinForms.HorizontalAlignment.Right,
        CENTER: WinForms.HorizontalAlignment.Center,
        JUSTIFY: WinForms.HorizontalAlignment.Left,
    }[value]


def add_handler(cmd):
    action = cmd.action

    def handler(sender, event):
        return action(None)

    return handler
