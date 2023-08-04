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
    supports_custom_fonts = False

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

        assert (BOLD if traits & UIFontDescriptorTraitBold else NORMAL) == weight

        if style == OBLIQUE:
            print("Interpreting OBLIQUE font as ITALIC")
            assert bool(traits & UIFontDescriptorTraitItalic)
        else:
            assert ITALIC if traits & UIFontDescriptorTraitItalic else NORMAL == style

        if variant == SMALL_CAPS:
            print("Ignoring SMALL CAPS font test")
        else:
            assert NORMAL == variant

    def assert_font_size(self, expected):
        if expected == SYSTEM_DEFAULT_FONT_SIZE:
            assert self.font.pointSize == 17
        else:
            assert self.font.pointSize == expected

    def assert_font_family(self, expected):
        assert str(self.font.familyName) == {
            CURSIVE: "Snell Roundhand",
            FANTASY: "Papyrus",
            MONOSPACE: "Courier New",
            SANS_SERIF: "Helvetica",
            SERIF: "Times New Roman",
            SYSTEM: ".AppleSystemUIFont",
            MESSAGE: ".AppleSystemUIFont",
        }.get(expected, expected)
