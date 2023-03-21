from System.Drawing import Color, ContentAlignment, SystemColors
from travertino.fonts import Font

from toga.colors import TRANSPARENT, rgba
from toga.fonts import BOLD, ITALIC, NORMAL
from toga.style.pack import CENTER, LEFT, RIGHT


def toga_color(color):
    if color in {Color.Empty, SystemColors.Control}:
        return TRANSPARENT
    else:
        return rgba(color.R, color.G, color.B, color.A / 255)


def toga_font(font):
    return Font(
        family=str(font.Name),
        size=int(font.SizeInPoints),
        style=ITALIC if font.Italic else NORMAL,
        variant=NORMAL,
        weight=BOLD if font.Bold else NORMAL,
    )


def toga_alignment(alignment):
    return {
        ContentAlignment.MiddleLeft: LEFT,
        ContentAlignment.MiddleRight: RIGHT,
        ContentAlignment.MiddleCenter: CENTER,
    }[alignment]
