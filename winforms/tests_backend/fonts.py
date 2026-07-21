from System.Drawing import FontFamily, SystemFonts
from tests.conftest import approx

from toga.fonts import (
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    NORMAL,
    OBLIQUE,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)


class FontMixin:
    supports_custom_fonts = True
    supports_custom_variable_fonts = True

    def preinstalled_font(self):
        return "Times New Roman"

    @property
    def font(self):
        return self.native.Font

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        assert weight == (BOLD if self.font.Bold else NORMAL)

        if style == OBLIQUE:
            print("Interpreting OBLIQUE font as ITALIC")
            assert self.font.Italic
        else:
            assert style == (ITALIC if self.font.Italic else NORMAL)

        if variant == SMALL_CAPS:
            print("Ignoring SMALL CAPS font test")
        else:
            assert variant == NORMAL

    @property
    def font_size(self):
        size_in_points = self.font.Size / self.scale_factor * 72 / 96
        # This is a hacky workaround.  We specify font sizes in pixels, so
        # there are rounding issues.  However, returning approximate values
        # here directly means that the result cannot be manipulated by
        # arithmetic before a comparison in dpi change tests.  Since all font
        # sizes are integers, we compare to the integer equivalent and return
        # that.
        assert approx(size_in_points) == round(size_in_points)
        return round(size_in_points)

    def assert_font_size(self, expected):
        if expected == SYSTEM_DEFAULT_FONT_SIZE:
            expected = 9
        assert self.font_size == expected

    def assert_font_family(self, expected):
        assert str(self.font.Name) == {
            CURSIVE: "Comic Sans MS",
            FANTASY: "Impact",
            MESSAGE: SystemFonts.MessageBoxFont.FontFamily.Name,
            MONOSPACE: FontFamily.GenericMonospace.Name,
            SANS_SERIF: FontFamily.GenericSansSerif.Name,
            SERIF: FontFamily.GenericSerif.Name,
            SYSTEM: SystemFonts.MessageBoxFont.FontFamily.Name,
        }.get(expected, expected)
