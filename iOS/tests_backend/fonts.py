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
from toga_iOS.libs import (
    UIFontDescriptorTraitBold,
    UIFontDescriptorTraitItalic,
)


class FontMixin:
    supports_custom_fonts = True
    supports_custom_variable_fonts = False

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
        elif isinstance(expected, str):
            base_size = 17
            if expected in RELATIVE_FONT_SIZES:
                # For relative sizes, we need to know the parent size
                # In tests, assume MEDIUM as the parent size if not specified
                parent_size = getattr(self, "_parent_size", base_size)
                expected_size = parent_size * RELATIVE_FONT_SIZE_SCALE.get(
                    expected, 1.0
                )
            else:
                expected_size = base_size * FONT_SIZE_SCALE.get(expected, 1.0)
            assert abs(self.font.pointSize - expected_size) < 0.01
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
