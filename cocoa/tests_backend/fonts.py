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
from toga_cocoa.libs.appkit import NSFontMask


class FontMixin:
    supports_custom_fonts = True
    supports_custom_variable_fonts = False

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        # Cocoa's FANTASY (Papyrus) and CURSIVE (Apple Chancery) system
        # fonts don't have any bold/italic variants.
        if str(self.font.familyName) == "Papyrus":
            print("Ignoring options on FANTASY system font")
            return
        elif str(self.font.familyName) == "Apple Chancery":
            print("Ignoring options on CURSIVE system font")
            return

        traits = self.font.fontDescriptor.symbolicTraits

        assert (BOLD if traits & NSFontMask.Bold else NORMAL) == weight

        if style == OBLIQUE:
            print("Interpreting OBLIQUE font as ITALIC")
            assert bool(traits & NSFontMask.Italic)
        else:
            assert ITALIC if traits & NSFontMask.Italic else NORMAL == style

        if variant == SMALL_CAPS:
            print("Ignoring SMALL CAPS font test")
        else:
            assert NORMAL == variant

    def assert_font_size(self, expected):
        if expected == SYSTEM_DEFAULT_FONT_SIZE:
            assert self.font.pointSize == 13
        else:
            assert self.font.pointSize == expected * 96 / 72

    def assert_font_family(self, expected):
        assert str(self.font.familyName) == {
            # System and Message fonts use internal names
            SYSTEM: ".AppleSystemUIFont",
            MESSAGE: ".AppleSystemUIFont",
            # Known fonts use pre-registered names
            CURSIVE: "Apple Chancery",
            FANTASY: "Papyrus",
            MONOSPACE: "Courier New",
            SANS_SERIF: "Helvetica",
            SERIF: "Times",
            # Most other fonts we can just use the family name;
            # however, the Font Awesome font has a different
            # internal Postscript name, which *doesn't* include
            # the "solid" weight component.
            "Font Awesome 5 Free Solid": "Font Awesome 5 Free",
        }.get(expected, expected)
