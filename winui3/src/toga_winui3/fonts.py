from win32more.Microsoft.UI.Xaml.Media import FontFamily
from win32more.Windows.UI.Text import FontStyle, FontWeight, FontWeights

from toga.fonts import (
    # MISC
    _IMPL_CACHE,
    _REGISTERED_FONT_CACHE,
    # FONT_WEIGHTS
    BOLD,
    # SYSTEM_DEFAULT_FONTS
    CURSIVE,
    FANTASY,
    # FONT_STYLES
    ITALIC,
    MESSAGE,
    MONOSPACE,
    OBLIQUE,
    SANS_SERIF,
    SERIF,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    UnknownFontError,
)

from .libs.gdiplus import is_font_installed


class NativeFont:
    def __init__(
        self,
        family: FontFamily | None,
        size: int | None,
        style: FontStyle,
        weight: FontWeight,
    ):
        """The Toga font attributes that can be set in WinUI 3.

        :param family: The font to use. A None value means that the system default
            will be used.
        :param font_size: The size (line height) of a font given in CSS pixels. A None
            value means that the system default will be used.
        :param font_style: The style of the font, e.g. normal, italic. Given as a
            FontStyle object.
        :param font_weight: The weight of the font, e.g. light, bold, etc. Given as a
            FontWeight object.
        """
        self.FontFamily = self._creator(family)
        self.FontSize = self._creator(size)
        self.FontStyle = self._creator(style)
        self.FontWeight = self._creator(weight)

    def _creator(self, property):
        def property_creator(property=property):
            return property

        return property_creator


class Font:
    def __init__(self, interface):
        """A Toga WinUI 3 font object created from the core interface.

        Notes about default settings:
        - The WinUI 3 implementation doesn't assume that system defaults for size and
            family are consistent across the UI. In the native classes, these properties
            are 'dependency properties' which means that they can be reset to default by
            clearing the set value.
        - Italics goes against the Windows design prinicpals, so it is safe to set the
            Normal font style by default. See:
            learn.microsoft.com/windows/apps/design/signature-experiences/typography

        """
        self.interface = interface

    ####################################################################################
    # Font loading
    ####################################################################################

    def load_predefined_system_font(self):
        """Use one of the system font names Toga predefines."""
        try:
            font_family = {
                SYSTEM: SYSTEM,
                MESSAGE: SYSTEM,
                SERIF: FontFamily("Times New Roman"),
                SANS_SERIF: FontFamily("Segoe UI"),
                CURSIVE: FontFamily("Segoe Script"),
                FANTASY: FontFamily("Impact"),
                MONOSPACE: FontFamily("Courier New"),
            }[self.interface.family]
        except KeyError as exc:
            msg = f"{self.interface} not a predefined system font"
            raise UnknownFontError(msg) from exc

        self._assign_native(font_family)

    def load_user_registered_font(self):
        """Use a font that has been registered in the user's code."""
        font_key = self.interface._registered_font_key(
            self.interface.family,
            weight=self.interface.weight,
            style=self.interface.style,
            variant=self.interface.variant,
        )
        try:
            font_path = _REGISTERED_FONT_CACHE[font_key]
        except KeyError as exc:
            msg = f"{self.interface} not a user-registered font"
            raise UnknownFontError(msg) from exc

        raise ValueError(
            f"Couldn't load {font_path}. User registered fonts are not implemented yet."
        )

    def load_arbitrary_system_font(self):
        """Use a font available on the system."""
        font_installed = is_font_installed(self.interface.family)

        # WinUI 3 does not throw an exception if the font is not installed, so use GDI+.
        if not font_installed:
            raise UnknownFontError(
                f"{self.interface} not installed on system. Check that the font family "
                + "name exactly matches the name in the system's font settings."
            )

        font_family = FontFamily(self.interface.family)
        self._assign_native(font_family)

    ####################################################################################
    # Assign loaded font
    ####################################################################################

    def _assign_native(self, font_family):
        # Font family
        if font_family == SYSTEM:
            family = None
        else:
            family = font_family

        # Font size
        if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
            size = None
        else:
            # Toga uses CSS points. Convert to CSS pixels.
            size = self.interface.size * 96 / 72

        # Font style
        if self.interface.style == ITALIC:
            style = FontStyle.Italic
        elif self.interface.style == OBLIQUE:
            style = FontStyle.Oblique
        else:
            style = FontStyle.Normal

        # Font weight
        if self.interface.weight == BOLD:
            weight = FontWeights.get_Bold()
        else:
            weight = FontWeights.get_Normal()

        self.native = NativeFont(family, size, style, weight)
        _IMPL_CACHE[self.interface] = self
