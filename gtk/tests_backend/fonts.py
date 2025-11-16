from toga.fonts import (
    NORMAL,
    SYSTEM_DEFAULT_FONT_SIZE,
)
from toga_gtk.libs import GTK_VERSION


class FontMixin:
    supports_custom_fonts = True
    supports_custom_variable_fonts = True

    def preinstalled_font(self):
        return "Liberation Serif"

    def assert_font_family(self, expected):
        assert self.font.family == expected

    def assert_font_size(self, expected):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # GTK fonts aren't realized until they appear on a widget.
            # The actual system default size is determined by the widget theme.
            # So - if the font size reports as 0, it must be a default system
            # font size that hasn't been realized yet. Once a font has been realized,
            # we can't reliably determine what the system font size is, other than
            # knowing that it must be non-zero. Pick some reasonable bounds instead.
            #
            # See also SYSTEM_DEFAULT_FONT_SIZE in toga_gtk/widgets/canvas.py.
            if self.font.size <= 0:
                assert expected == SYSTEM_DEFAULT_FONT_SIZE
            elif expected == SYSTEM_DEFAULT_FONT_SIZE:
                assert 8 < int(self.font.size) < 18
            else:
                assert int(self.font.size) == expected
        else:  # pragma: no-cover-if-gtk3
            assert int(self.font.size) == expected

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        assert self.font.weight == weight
        assert self.font.style == style
        assert self.font.variant == variant
