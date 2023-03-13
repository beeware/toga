from java import jint
from travertino.fonts import Font

from android.graphics import Color, Typeface
from android.util import TypedValue
from toga.colors import TRANSPARENT, rgba
from toga.fonts import (
    BOLD,
    ITALIC,
    NORMAL,
    SYSTEM,
)


def toga_color(color_int):
    # Select the `int` overloads rather than the `long` ones.
    color_int = jint(color_int)
    if color_int == 0:
        return TRANSPARENT
    else:
        return rgba(
            Color.red(color_int),
            Color.green(color_int),
            Color.blue(color_int),
            Color.alpha(color_int) / 255,
        )


DECLARED_FONTS = None


def load_fontmap():
    global DECLARED_FONTS
    field = Typeface.getClass().getDeclaredField("sSystemFontMap")
    field.setAccessible(True)

    fontmap = field.get(None)
    DECLARED_FONTS = {fontmap.get(key): key for key in fontmap.keySet().toArray()}


def toga_font(typeface, size, resources):
    # Android provides font details in pixels; that size needs to be converted to SP (see
    # notes in toga_android/fonts.py).
    pixels_per_sp = TypedValue.applyDimension(
        TypedValue.COMPLEX_UNIT_SP, 1, resources.getDisplayMetrics()
    )

    # Ensure we have a map of typeface to font names
    if DECLARED_FONTS is None:
        load_fontmap()

    return Font(
        family=SYSTEM if typeface == Typeface.DEFAULT else DECLARED_FONTS[typeface],
        size=round(size / pixels_per_sp),
        style=ITALIC if typeface.isItalic() else NORMAL,
        variant=NORMAL,
        weight=BOLD if typeface.isBold() else NORMAL,
    )
