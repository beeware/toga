from System.Drawing import FontFamily, SystemFonts

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
        return round(self.font.SizeInPoints / self.scale_factor)

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
