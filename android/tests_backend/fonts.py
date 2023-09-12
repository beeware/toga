from android.graphics import Typeface
from android.util import TypedValue
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


class FontMixin:
    supports_custom_fonts = True

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
            assert NORMAL == variant

    def assert_font_size(self, expected):
        if expected == SYSTEM_DEFAULT_FONT_SIZE:
            expected = self.default_font_size
        assert round(self.text_size) == round(
            TypedValue.applyDimension(
                TypedValue.COMPLEX_UNIT_SP,
                expected,
                self.native.getResources().getDisplayMetrics(),
            )
        )

    def assert_font_family(self, expected):
        # Ensure we have a map of typeface to font names
        if not DECLARED_FONTS:
            load_fontmap()

        assert DECLARED_FONTS[self.typeface] == {
            SYSTEM: self.default_font_family,
            MESSAGE: "sans-serif",
        }.get(expected, expected)
