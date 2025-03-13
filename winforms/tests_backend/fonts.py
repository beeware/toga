from System.Drawing import FontFamily, SystemFonts
from travertino.constants import (
    FONT_SIZE_SCALE,
    RELATIVE_FONT_SIZE_SCALE,
    RELATIVE_FONT_SIZES,
)

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

    @property
    def font(self):
        return self.native.Font

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        assert BOLD if self.font.Bold else NORMAL == weight

        if style == OBLIQUE:
            print("Interpreting OBLIQUE font as ITALIC")
            assert self.font.Italic
        else:
            assert (ITALIC if self.font.Italic else NORMAL) == style

        if variant == SMALL_CAPS:
            print("Ignoring SMALL CAPS font test")
        else:
            assert NORMAL == variant

    @property
    def font_size(self):
        return round(self.font.SizeInPoints / self.scale_factor)

    def assert_font_size(self, expected):
        if expected == SYSTEM_DEFAULT_FONT_SIZE:
            expected = 9.0
        elif isinstance(expected, str):
            base_size = 9.0
            if expected in RELATIVE_FONT_SIZES:
                parent_size = getattr(self, "_parent_size", base_size)
                expected = parent_size * RELATIVE_FONT_SIZE_SCALE.get(expected, 1.0)
            else:
                expected = base_size * FONT_SIZE_SCALE.get(expected, 1.0)
        assert abs(self.font.SizeInPoints - expected) < 0.1

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
