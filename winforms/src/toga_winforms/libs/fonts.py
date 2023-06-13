from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from .winforms import (
    ContentAlignment,
    WinForms,
)


def TextAlignment(value):
    return {
        LEFT: ContentAlignment.TopLeft,
        RIGHT: ContentAlignment.TopRight,
        CENTER: ContentAlignment.TopCenter,
        JUSTIFY: ContentAlignment.TopLeft,
    }[value]


# Justify simply sets Left alignment. Is this the best option?
def HorizontalTextAlignment(value):
    return {
        LEFT: WinForms.HorizontalAlignment.Left,
        RIGHT: WinForms.HorizontalAlignment.Right,
        CENTER: WinForms.HorizontalAlignment.Center,
        JUSTIFY: WinForms.HorizontalAlignment.Left,
    }[value]
