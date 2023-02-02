from travertino.fonts import Font

from toga.colors import rgba
from toga.fonts import FANTASY, NORMAL, SYSTEM
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT
from toga_cocoa.libs.appkit import (
    NSCenterTextAlignment,
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
    return Font(
        family={
            ".AppleSystemUIFont": SYSTEM,
            "Papyrus": FANTASY,
        }.get(str(font.familyName), str(font.familyName)),
        size=font.pointSize,
        style=NORMAL,  # TODO: ITALIC if..., SMALL_CAPS if ...
        variant=NORMAL,
        weight=NORMAL,  # TODO: BOLD if ...
    )


def toga_alignment(alignment):
    return {
        NSLeftTextAlignment: LEFT,
        NSRightTextAlignment: RIGHT,
        NSCenterTextAlignment: CENTER,
        NSJustifiedTextAlignment: JUSTIFY,
    }[alignment]
