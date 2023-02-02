from ctypes import byref
from dataclasses import dataclass

from pytest import skip
from rubicon.objc import CGFloat

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
        skip("Can't convert UIColor to toga color yet")
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


@dataclass
class Font:
    family: str
    size: int
    style: str = NORMAL
    variant: str = NORMAL
    weight: str = NORMAL


def toga_font(font):
    return Font(
        family={
            ".AppleSystemUIFont": SYSTEM,
            "Papyrus": FANTASY,
        }.get(str(font.familyName), str(font.familyName)),
        size=font.pointSize,
    )


def toga_alignment(alignment):
    return {
        NSLeftTextAlignment: LEFT,
        NSRightTextAlignment: RIGHT,
        NSCenterTextAlignment: CENTER,
        NSJustifiedTextAlignment: JUSTIFY,
    }[alignment]
