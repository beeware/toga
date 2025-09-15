import pytest

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
from toga_iOS.libs import (
    UIFontDescriptorTraitBold,
    UIFontDescriptorTraitItalic,
)


class FontMixin:
    supports_custom_fonts = True
    supports_custom_variable_fonts = False

    def preinstalled_font(self):
        pytest.skip("Use of arbitrary system fonts is not yet supported on iOS.")

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        # Cocoa's FANTASY (Papyrus) and CURSIVE (Snell Roundhand) system
        # fonts don't have any bold/italic variants.
        if str(self.font.familyName) == "Papyrus":
            print("Ignoring options on FANTASY system font")
            return
        elif str(self.font.familyName) == "Snell Roundhand":
            print("Ignoring options on CURSIVE system font")
            return

        traits = self.font.fontDescriptor.symbolicTraits

        assert weight == (BOLD if traits & UIFontDescriptorTraitBold else NORMAL)

        if style == OBLIQUE:
            print("Interpreting OBLIQUE font as ITALIC")
            assert bool(traits & UIFontDescriptorTraitItalic)
        else:
            assert style == (ITALIC if traits & UIFontDescriptorTraitItalic else NORMAL)

        if variant == SMALL_CAPS:
            print("Ignoring SMALL CAPS font test")
        else:
            assert variant == NORMAL

    def assert_font_size(self, expected):
        if expected == SYSTEM_DEFAULT_FONT_SIZE:
            assert self.font.pointSize == 17
        else:
            assert self.font.pointSize == expected * 96 / 72

    def assert_font_family(self, expected):
        assert str(self.font.familyName) == {
            # System and Message fonts use internal names
            SYSTEM: ".AppleSystemUIFont",
            MESSAGE: ".AppleSystemUIFont",
            # Known fonts use pre-registered names
            CURSIVE: "Snell Roundhand",
            FANTASY: "Papyrus",
            MONOSPACE: "Courier New",
            SANS_SERIF: "Helvetica",
            SERIF: "Times New Roman",
            # Most other fonts we can just use the family name;
            # however, the Font Awesome font has a different
            # internal Postscript name, which *doesn't* include
            # the "solid" weight component.
            "Font Awesome 5 Free Solid": "Font Awesome 5 Free",
        }.get(expected, expected)
