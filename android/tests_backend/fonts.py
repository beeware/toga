from concurrent.futures import ThreadPoolExecutor

import pytest
from android.graphics import Typeface
from android.graphics.fonts import FontFamily
from android.util import TypedValue
from fontTools.ttLib import TTFont
from java import jint
from java.lang import Integer, Long

from toga.fonts import (
    BOLD,
    ITALIC,
    MESSAGE,
    NORMAL,
    OBLIQUE,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)

SYSTEM_FONTS = {}
nativeGetFamily = new_FontFamily = None


def load_fontmap():
    field = Typeface.getClass().getDeclaredField("sSystemFontMap")
    field.setAccessible(True)
    fontmap = field.get(None)

    for name in fontmap.keySet().toArray():
        typeface = fontmap.get(name)
        SYSTEM_FONTS[typeface] = name
        for native_style in [
            Typeface.BOLD,
            Typeface.ITALIC,
            Typeface.BOLD | Typeface.ITALIC,
        ]:
            SYSTEM_FONTS[Typeface.create(typeface, native_style)] = name


def reflect_font_methods():
    global nativeGetFamily, new_FontFamily

    # Bypass non-SDK interface restrictions by looking them up on a background thread
    # with no Java stack frames (https://stackoverflow.com/a/61600526).
    with ThreadPoolExecutor() as executor:
        nativeGetFamily = executor.submit(
            Typeface.getClass().getDeclaredMethod,
            "nativeGetFamily",
            Long.TYPE,
            Integer.TYPE,
        ).result()
        nativeGetFamily.setAccessible(True)

        new_FontFamily = executor.submit(
            FontFamily.getClass().getConstructor, Long.TYPE
        ).result()


class FontMixin:
    supports_custom_fonts = True
    supports_custom_variable_fonts = True

    def preinstalled_font(self):
        pytest.skip("Use of arbitrary system fonts is not yet supported on Android.")

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        assert (BOLD if self.typeface.isBold() else NORMAL) == weight

        if style == OBLIQUE:
            print("Interpreting OBLIQUE font as ITALIC")
            assert self.typeface.isItalic()
        else:
            assert (ITALIC if self.typeface.isItalic() else NORMAL) == style

        if variant == SMALL_CAPS:
            print("Ignoring SMALL CAPS font test")
        else:
            assert variant == NORMAL

    def assert_font_size(self, expected):
        if expected == SYSTEM_DEFAULT_FONT_SIZE:
            expected = self.default_font_size * (72 / 96)
        assert round(self.text_size) == round(
            TypedValue.applyDimension(
                TypedValue.COMPLEX_UNIT_SP,
                expected * (96 / 72),
                self.native.getResources().getDisplayMetrics(),
            )
        )

    def assert_font_family(self, expected):
        if not SYSTEM_FONTS:
            load_fontmap()

        if actual := SYSTEM_FONTS.get(self.typeface):
            assert actual == {
                SYSTEM: self.default_font_family,
                MESSAGE: "sans-serif",
            }.get(expected, expected)
        else:
            if not nativeGetFamily:
                reflect_font_methods()
            family_ptr = nativeGetFamily.invoke(
                None, self.typeface.native_instance, jint(0)
            )
            family = new_FontFamily.newInstance(family_ptr)
            assert family.getSize() == 1

            font = TTFont(family.getFont(0).getFile().getPath())
            assert font["name"].getDebugName(1) == expected
