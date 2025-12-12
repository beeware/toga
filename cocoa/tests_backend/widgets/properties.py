from toga.colors import rgb
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT
from toga_cocoa.libs.appkit import (
    NSCenterTextAlignment,
    NSJustifiedTextAlignment,
    NSLeftTextAlignment,
    NSRightTextAlignment,
)


def toga_color(color):
    if color:
        return rgb(
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
