from java import jint
from travertino.fonts import Font

from android.graphics import Color, Typeface
from android.util import TypedValue
from toga.colors import rgba
from toga.fonts import BOLD, ITALIC, MONOSPACE, NORMAL, SANS_SERIF, SERIF, SYSTEM


def toga_color(color_int):
    # Select the `int` overloads rather than the `long` ones.
    color_int = jint(color_int)
    return rgba(
        Color.red(color_int),
        Color.green(color_int),
        Color.blue(color_int),
        Color.alpha(color_int) / 255,
    )


def toga_font(typeface, size, resources):
    # Android provides font details in pixels; that size needs to be converted to points.
    pixels_per_point = TypedValue.applyDimension(
        TypedValue.COMPLEX_UNIT_PT, 1, resources.getDisplayMetrics()
    )

    return Font(
        family={
            Typeface.DEFAULT: SYSTEM,
            Typeface.MONOSPACE: MONOSPACE,
            Typeface.SANS_SERIF: SANS_SERIF,
            Typeface.SERIF: SERIF,
            # : CURSIVE ??
            # : FANTASY ??
        }.get(typeface, "Unknown"),
        size=size / pixels_per_point,
        style=ITALIC if typeface.isItalic() else NORMAL,
        variant=NORMAL,
        weight=BOLD if typeface.isBold() else NORMAL,
    )
