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
from toga_cocoa.libs.appkit import NSFont, NSFontMask


class FontMixin:
    supports_custom_fonts = False

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
            assert self.font.pointSize == NSFont.systemFontSize
        else:
            assert self.font.pointSize == expected

    def assert_font_family(self, expected):
        assert str(self.font.familyName) == {
            CURSIVE: "Apple Chancery",
            FANTASY: "Papyrus",
            MONOSPACE: "Courier New",
            SANS_SERIF: "Helvetica",
            SERIF: "Times",
            SYSTEM: ".AppleSystemUIFont",
            MESSAGE: ".AppleSystemUIFont",
        }.get(expected, expected)
