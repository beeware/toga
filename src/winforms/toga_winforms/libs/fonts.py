from .winforms import ContentAlignment, FontFamily, WinForms, SystemFonts, Text, FontStyle

from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY
from toga.fonts import (
    MESSAGE,
    SYSTEM,
    SERIF,
    SANS_SERIF,
    SYSTEM_DEFAULT_SIZE,
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
    try:
        return {
            SYSTEM: SystemFonts.DefaultFont.FontFamily,
            MESSAGE: SystemFonts.MenuFont.FontFamily,
            SERIF: FontFamily.GenericSerif,
            SANS_SERIF: FontFamily.GenericSansSerif,
            CURSIVE: FontFamily("Comic Sans MS"),
            FANTASY: FontFamily("Impact"),
            MONOSPACE: FontFamily.GenericMonospace,
        }[value]
    except KeyError:
        if value in Text.InstalledFontCollection().Families:
            return FontFamily(value)
    else:
        print(
            "Unable to load font-family '{}', loading {} instead".format(
                value, SystemFonts.DefaultFont.FontFamily)
        )
        return SystemFonts.DefaultFont.FontFamily


def win_font_style(weight, style, font_family):
    font_style = FontStyle.Regular
    if weight.lower() == "bold" and font_family.IsStyleAvailable(
            FontStyle.Bold):
        font_style += FontStyle.Bold
    if style.lower() == "italic" and font_family.IsStyleAvailable(
            FontStyle.Italic):
        font_style += FontStyle.Italic
    return font_style


def win_font_size(size):
    if size == SYSTEM_DEFAULT_SIZE:
        return SystemFonts.DefaultFont.Size
    return size
