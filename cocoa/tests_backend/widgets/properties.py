from toga.colors import TRANSPARENT, rgba
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT
from toga_cocoa.libs.appkit import (
    NSCenterTextAlignment,
    NSColor,
    NSJustifiedTextAlignment,
    NSLeftTextAlignment,
    NSRightTextAlignment,
)


def toga_color(color):
    if color:
        # Equivalent to setting no color at all, aka. default color.
        # Which of the below two is used is dependent on the widget.
        if color == NSColor.controlTextColor or color == NSColor.labelColor:
            return None
        elif color == NSColor.clearColor:
            return TRANSPARENT
        return rgba(
            color.redComponent * 255,
            color.greenComponent * 255,
            color.blueComponent * 255,
            color.alphaComponent,
        )
    else:
        return None


def toga_text_align(alignment):
    return {
        NSLeftTextAlignment: LEFT,
        NSRightTextAlignment: RIGHT,
        NSCenterTextAlignment: CENTER,
        NSJustifiedTextAlignment: JUSTIFY,
    }[alignment]
