from System import ArgumentException
from System.Drawing import (
    Font as WinFont,
    FontFamily,
    FontStyle,
    SystemFonts,
)
from System.Drawing.Text import PrivateFontCollection
from System.IO import FileNotFoundException
from System.Runtime.InteropServices import ExternalException

from toga.fonts import (
    _IMPL_CACHE,
    _REGISTERED_FONT_CACHE,
    CURSIVE,
    FANTASY,
    MESSAGE,
    MONOSPACE,
    SANS_SERIF,
    SERIF,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    UnknownFontError,
)

# Unlike SystemFonts.DefaultFont, MessageBoxFont respects the system theme
# (https://github.com/dotnet/winforms/issues/524).
DEFAULT_FONT = SystemFonts.MessageBoxFont


class Font:
    def __init__(self, interface):
        # this needs to be an instance variable, otherwise we might get Winforms
        # exceptions later
        self._pfc = None
        self.interface = interface

    def load_predefined_system_font(self):
        """Use one of the system font names Toga predefines."""
        try:
            font_family = {
                SYSTEM: DEFAULT_FONT.FontFamily,
                MESSAGE: DEFAULT_FONT.FontFamily,
                SERIF: FontFamily.GenericSerif,
                SANS_SERIF: FontFamily.GenericSansSerif,
                CURSIVE: FontFamily("Comic Sans MS"),
                FANTASY: FontFamily("Impact"),
                MONOSPACE: FontFamily.GenericMonospace,
            }[self.interface.family]
        except KeyError as exc:
            msg = f"{self.interface} not a predefined system font"
            raise UnknownFontError(msg) from exc

        self._assign_native(font_family)

    def load_user_registered_font(self):
        """Use a font that the user has registered in their code."""
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

        # Yes, user has registered this font.
        self._pfc = PrivateFontCollection()
        try:
            self._pfc.AddFontFile(font_path)
            font_family = self._pfc.Families[0]

        except FileNotFoundException as exc:
            raise ValueError(f"Font file {font_path} could not be found") from exc
        except (IndexError, ExternalException) as exc:
            raise ValueError(f"Unable to load font file {font_path}") from exc

        self._assign_native(font_family)

    def load_arbitrary_system_font(self):
        """Use a font available on the system."""
        try:
            # Check for a font installed on the system.
            font_family = FontFamily(self.interface.family)
        except ArgumentException as exc:
            msg = f"{self.interface} not found installed on system"
            raise UnknownFontError(msg) from exc

        self._assign_native(font_family)

    def _assign_native(self, font_family):
        # Convert font style to Winforms format
        font_style = FontStyle.Regular
        if self.interface.weight == "bold" and font_family.IsStyleAvailable(
            FontStyle.Bold
        ):
            font_style |= FontStyle.Bold
        if (
            # Winforms doesn't recognize Oblique; so we interpret as Italic
            self.interface.style in {"italic", "oblique"}
            and font_family.IsStyleAvailable(FontStyle.Italic)
        ):
            font_style |= FontStyle.Italic

        # Convert font size to Winforms format
        if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
            font_size = DEFAULT_FONT.Size
        else:
            font_size = self.interface.size

        self.native = WinFont(font_family, font_size, font_style)
        _IMPL_CACHE[self.interface] = self

    def metric(self, name):
        """Return the given metric, measured in CSS pixels."""
        family = self.native.FontFamily
        style = self.native.Style
        em_height = self.native.SizeInPoints * 96 / 72
        design_unit = em_height / family.GetEmHeight(style)
        return design_unit * getattr(family, f"Get{name}")(style)
