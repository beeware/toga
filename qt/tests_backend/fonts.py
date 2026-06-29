from PySide6.QtGui import QFont, QFontDatabase

from toga.fonts import (
    BOLD,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    NORMAL,
    OBLIQUE,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)


class FontMixin:
    supports_custom_fonts = True
    supports_custom_variable_fonts = True

    def preinstalled_font(self):
        # grab a known font family
        return QFontDatabase.families()[0]

    def assert_font_family(self, expected):
        assert self.font.family() == {
            # System fonts supplied by QFontDatabase
            SYSTEM: QFontDatabase.systemFont(
                QFontDatabase.SystemFont.GeneralFont
            ).family(),
            MESSAGE: QFontDatabase.systemFont(
                QFontDatabase.SystemFont.GeneralFont
            ).family(),
            MONOSPACE: QFontDatabase.systemFont(
                QFontDatabase.SystemFont.FixedFont
            ).family(),
            # Most other fonts we can just use the family name;
            # however, the Font Awesome font has a different
            # internal Postscript name, which *doesn't* include
            # the "solid" weight component.
            "Font Awesome 5 Free Solid": "Font Awesome 5 Free",
        }.get(expected, expected)

    def assert_font_size(self, expected):
        if expected != SYSTEM_DEFAULT_FONT_SIZE:
            assert self.font.pointSizeF() == expected

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        assert (
            self.font.weight() == QFont.Weight.Bold
            if weight == BOLD
            else QFont.Weight.Normal
        )
        assert self.font.style() == {
            ITALIC: QFont.Style.StyleItalic,
            OBLIQUE: QFont.Style.StyleOblique,
        }.get(style, QFont.Style.StyleNormal)
        assert self.font.capitalization() == (
            QFont.Capitalization.SmallCaps
            if variant == SMALL_CAPS
            else QFont.Capitalization.MixedCase
        )
