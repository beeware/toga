from ctypes import byref

from rubicon.objc import CGFloat
from travertino.fonts import Font

from toga.colors import rgba
from toga.fonts import FANTASY, NORMAL, SYSTEM
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT
from toga_iOS.libs import (
    NSCenterTextAlignment,
    NSJustifiedTextAlignment,
    NSLeftTextAlignment,
    NSRightTextAlignment,
)


def toga_color(color):
    if color:
        red = CGFloat()
        green = CGFloat()
        blue = CGFloat()
        alpha = CGFloat()
        color.getRed(
            byref(red), green=byref(green), blue=byref(blue), alpha=byref(alpha)
        )
        return rgba(red.value * 255, green.value * 255, blue.value * 255, alpha.value)
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
