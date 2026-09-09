from toga_winui3.widgets.properties.native import get_attribute_base
from win32more.Windows.UI.Text import FontStyle, FontWeights

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
    supports_custom_fonts = False
    supports_custom_variable_fonts = True

    def preinstalled_font(self):
        """A font known to be installed on the system."""
        return "Arial"

    @property
    def font_family(self):
        return self.native.FontFamily

    @property
    def font_size(self):
        return self.native.FontSize

    @property
    def font_style(self):
        return self.native.FontStyle

    @property
    def font_weight(self):
        return self.native.FontWeight

    @property
    def native_cls(self):
        return type(self.native)

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        # Font weight.
        if weight == BOLD:
            assert self.font_weight.Weight == FontWeights.get_Bold().Weight
        else:
            assert weight == NORMAL
            assert self.font_weight.Weight == FontWeights.get_Normal().Weight

        # Font style
        if style == OBLIQUE:
            assert self.font_style == FontStyle.Oblique
        elif style == ITALIC:
            assert self.font_style == FontStyle.Italic
        else:
            assert style == NORMAL
            assert self.font_style == FontStyle.Normal

        # Font variant
        if variant == SMALL_CAPS:
            print("Ignoring SMALL CAPS font test")
        else:
            assert variant == NORMAL

    def assert_font_size(self, expected):
        if expected == SYSTEM_DEFAULT_FONT_SIZE:
            # Store current size
            current_size = self.font_size

            # Reset size to the default value
            native_cls = self.native_cls
            dependency_ancestor = get_attribute_base(native_cls, "FontSizeProperty")
            dependency_attribute = dependency_ancestor.FontSizeProperty
            self.native.ClearValue(dependency_attribute)

            assert self.font_size == current_size
        else:
            assert round(self.font_size, 2) == round(expected * 96 / 72, 2)

    def assert_font_family(self, expected):
        assert str(self.font_family.Source) == {
            CURSIVE: "Segoe Script",
            FANTASY: "Impact",
            MESSAGE: "Segoe UI Variable",
            MONOSPACE: "Courier New",
            SANS_SERIF: "Segoe UI",
            SERIF: "Times New Roman",
            SYSTEM: "Segoe UI Variable",
        }.get(expected, expected)
