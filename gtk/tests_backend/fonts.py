from toga.fonts import (
    NORMAL,
)


class FontMixin:
    supports_custom_fonts = True
    supports_custom_variable_fonts = True

    def preinstalled_font(self):
        return "Liberation Serif"

    def assert_font_family(self, expected):
        assert self.font.family == expected

    def assert_font_size(self, expected):
        assert int(self.font.size) == expected

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        assert self.font.weight == weight
        assert self.font.style == style
        assert self.font.variant == variant
