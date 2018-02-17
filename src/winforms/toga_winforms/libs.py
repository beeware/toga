from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY

import clr
clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms
from System import Decimal as ClrDecimal
from System import Convert
from System import Threading
from System import Uri
from System.Drawing import Size, Point, Color, ContentAlignment


def TextAlignment(value):
    return {
        LEFT: ContentAlignment.MiddleLeft,
        RIGHT: ContentAlignment.MiddleRight,
        CENTER: ContentAlignment.MiddleCenter,
        JUSTIFY: ContentAlignment.MiddleLeft,
    }[value]
