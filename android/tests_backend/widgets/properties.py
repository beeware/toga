from java import jint
from travertino.fonts import Font

from android.graphics import Color, Typeface
from android.os import Build
from android.text import Layout
from android.util import TypedValue
from android.view import Gravity
from toga.colors import TRANSPARENT, rgba
from toga.constants import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP
from toga.fonts import (
    BOLD,
    ITALIC,
    NORMAL,
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


DECLARED_FONTS = {}


def load_fontmap():
    field = Typeface.getClass().getDeclaredField("sSystemFontMap")
    field.setAccessible(True)
    fontmap = field.get(None)

    for name in fontmap.keySet().toArray():
        typeface = fontmap.get(name)
        DECLARED_FONTS[typeface] = name
        for native_style in [
            Typeface.BOLD,
            Typeface.ITALIC,
            Typeface.BOLD | Typeface.ITALIC,
        ]:
            DECLARED_FONTS[Typeface.create(typeface, native_style)] = name


def toga_font(typeface, size, resources):
    # Android provides font details in pixels; that size needs to be converted to SP (see
    # notes in toga_android/fonts.py).
    pixels_per_sp = TypedValue.applyDimension(
        TypedValue.COMPLEX_UNIT_SP, 1, resources.getDisplayMetrics()
    )

    # Ensure we have a map of typeface to font names
    if not DECLARED_FONTS:
        load_fontmap()

    return Font(
        family=DECLARED_FONTS[typeface],
        size=round(size / pixels_per_sp),
        style=ITALIC if typeface.isItalic() else NORMAL,
        variant=NORMAL,
        weight=BOLD if typeface.isBold() else NORMAL,
    )


def toga_alignment(gravity, justification_mode=None):
    horizontal_gravity = gravity & Gravity.HORIZONTAL_GRAVITY_MASK
    if (Build.VERSION.SDK_INT < 26) or (
        justification_mode in (None, Layout.JUSTIFICATION_MODE_NONE)
    ):
        return {
            Gravity.LEFT: LEFT,
            Gravity.RIGHT: RIGHT,
            Gravity.CENTER_HORIZONTAL: CENTER,
        }[horizontal_gravity]
    elif (
        justification_mode == Layout.JUSTIFICATION_MODE_INTER_WORD
        and horizontal_gravity == Gravity.LEFT
    ):
        return JUSTIFY
    else:
        raise ValueError(f"unknown combination: {gravity=}, {justification_mode=}")


def toga_vertical_alignment(gravity):
    vertical_gravity = gravity & Gravity.VERTICAL_GRAVITY_MASK
    return {
        Gravity.TOP: TOP,
        Gravity.BOTTOM: BOTTOM,
        Gravity.CENTER_VERTICAL: CENTER,
    }[vertical_gravity]
