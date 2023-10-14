from ctypes import byref

from rubicon.objc import CGFloat

from toga.colors import TRANSPARENT, rgba
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT
from toga_iOS.libs import (
    NSCenterTextAlignment,
    NSJustifiedTextAlignment,
    NSLeftTextAlignment,
    NSRightTextAlignment,
    UIColor,
)


def toga_color(color):
    if color:
        # Label color is a default foregroud value, equivalent to setting `color=None`
        if color == UIColor.labelColor():
            return None
        elif color == UIColor.clearColor:
            return TRANSPARENT

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


def toga_alignment(alignment):
    return {
        NSLeftTextAlignment: LEFT,
        NSRightTextAlignment: RIGHT,
        NSCenterTextAlignment: CENTER,
        NSJustifiedTextAlignment: JUSTIFY,
    }[alignment]
