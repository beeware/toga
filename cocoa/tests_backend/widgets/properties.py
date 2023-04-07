from travertino.fonts import Font

from toga.colors import rgba
from toga.fonts import BOLD, ITALIC, NORMAL
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT
from toga_cocoa.libs.appkit import (
    NSCenterTextAlignment,
    NSFontMask,
    NSJustifiedTextAlignment,
    NSLeftTextAlignment,
    NSRightTextAlignment,
)


def toga_color(color):
    if color:
        return rgba(
            color.redComponent * 255,
            color.greenComponent * 255,
            color.blueComponent * 255,
            color.alphaComponent,
        )
    else:
        return None


def toga_font(font):
    traits = font.fontDescriptor.symbolicTraits
    return Font(
        family=str(font.familyName),
        size=font.pointSize,
        style=ITALIC if traits & NSFontMask.Italic else NORMAL,
        variant=NORMAL,
        weight=BOLD if traits & NSFontMask.Bold else NORMAL,
    )


def toga_alignment(alignment):
    return {
        NSLeftTextAlignment: LEFT,
        NSRightTextAlignment: RIGHT,
        NSCenterTextAlignment: CENTER,
        NSJustifiedTextAlignment: JUSTIFY,
    }[alignment]
