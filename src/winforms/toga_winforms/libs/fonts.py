from .winforms import ContentAlignment, FontFamily, WinForms, SystemFonts, Text

from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY
from toga.fonts import (
    MESSAGE,
    SYSTEM,
    SERIF,
    SANS_SERIF,
    CURSIVE,
    FANTASY,
    MONOSPACE,
)


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
