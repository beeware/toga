from toga.fonts import (
    BOLD,
    ITALIC,
    NORMAL,
    OBLIQUE,
    SMALL_CAPS,
    SYSTEM_DEFAULT_FONT_SIZE,
)
from toga_gtk.libs import Pango


class FontMixin:
    supports_custom_fonts = True
    supports_custom_variable_fonts = True

    def assert_font_family(self, expected):
        assert self.font.family == expected

    def assert_font_size(self, expected):
        # GTK fonts aren't realized until they appear on a widget.
        # The actual system default size is determined by the widget theme.
        # So - if the font size reports as 0, it must be a default system
        # font size that hasn't been realized yet. Once a font has been realized,
        # we can't reliably determine what the system font size is, other than
        # knowing that it must be non-zero. Pick some reasonable bounds instead.
        #
        # See also SYSTEM_DEFAULT_FONT_SIZE in toga_gtk/widgets/canvas.py.
        if self.font.size == 0:
            assert expected == SYSTEM_DEFAULT_FONT_SIZE
        elif expected == SYSTEM_DEFAULT_FONT_SIZE:
            assert 8 < int(self.font.size) < 18
        else:
            assert int(self.font.size) == expected

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        assert {
            Pango.Weight.BOLD: BOLD,
        }.get(self.font.weight, NORMAL) == weight

        assert {
            Pango.Style.ITALIC: ITALIC,
            Pango.Style.OBLIQUE: OBLIQUE,
        }.get(self.font.style, NORMAL) == style

        assert {
            Pango.Variant.SMALL_CAPS: SMALL_CAPS,
        }.get(self.font.variant, NORMAL) == variant
