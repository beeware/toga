import clr
clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms  # noqa: E402
from System import Decimal as ClrDecimal  # noqa: E402, F401
from System import Convert  # noqa: E402, F401
from System import DateTime as WinDateTime  # noqa: E402, F401
from System import Threading  # noqa: E402, F401
from System import Uri  # noqa: E402, F401
from System.Drawing import Size, Point, Color, ContentAlignment, Bitmap  # noqa: E402
from System.Drawing import Icon as WinIcon  # noqa: E402, F401
from System.Drawing import Image as WinImage  # noqa: E402, F401
from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY  # noqa: E402


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
