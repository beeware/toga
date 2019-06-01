import ctypes

import clr

clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms  # noqa: E402
from System import Decimal as ClrDecimal  # noqa: E402, F401
from System import Single  # noqa: E402, F401
from System import Convert  # noqa: E402, F401
from System import DateTime as WinDateTime  # noqa: E402, F401
from System import Threading  # noqa: E402, F401
from System import Uri  # noqa: E402, F401
from System import Environment  # noqa: E402, F401

from System.Drawing import Icon as WinIcon  # noqa: E402, F401
from System.Drawing import Image as WinImage  # noqa: E402, F401
from System.Drawing import Font as WinFont  # noqa: E402, F401
from System.Drawing import ContentAlignment, Size, Point  # noqa: E402, F401
from System.Drawing import FontFamily, FontStyle, SystemFonts  # noqa: E402, F401
from System.Drawing import Text, Color, Bitmap  # noqa: E402, F401
from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY  # noqa: E402
from toga.fonts import (
    MESSAGE,
    SYSTEM,
    SERIF,
    SANS_SERIF,
    CURSIVE,
    FANTASY,
    MONOSPACE,
)  # noqa: E402

user32 = ctypes.windll.user32
win_version = Environment.OSVersion.Version.Major


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


def win_font_family(value):
    win_families = {
        SYSTEM: SystemFonts.DefaultFont.FontFamily,
        MESSAGE: SystemFonts.MenuFont.FontFamily,
        SERIF: FontFamily.GenericSerif,
        SANS_SERIF: FontFamily.GenericSansSerif,
        CURSIVE: FontFamily("Comic Sans MS"),
        FANTASY: FontFamily("Impact"),
        MONOSPACE: FontFamily.GenericMonospace,
    }
    for key in win_families:
        if value in key:
            return win_families[key]
    if value in Text.InstalledFontCollection().Families:
        return FontFamily(value)
    else:
        print(
            "Unable to load font-family '{}', loading {} instead".format(
                value, SystemFonts.DefaultFont.FontFamily)
        )
        return SystemFonts.DefaultFont.FontFamily
