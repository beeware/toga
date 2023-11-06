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
    _REGISTERED_FONT_CACHE,
    CURSIVE,
    FANTASY,
    MESSAGE,
    MONOSPACE,
    SANS_SERIF,
    SERIF,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)

_FONT_CACHE = {}

# Unlike SystemFonts.DefaultFont, MessageBoxFont respects the system theme
# (https://github.com/dotnet/winforms/issues/524).
DEFAULT_FONT = SystemFonts.MessageBoxFont


class Font:
    def __init__(self, interface):
        self._pfc = None  # this needs to be an instance variable, otherwise we might get Winforms exceptions later
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            font = None
            font_key = self.interface._registered_font_key(
                self.interface.family,
                weight=self.interface.weight,
                style=self.interface.style,
                variant=self.interface.variant,
            )
            try:
                font_path = _REGISTERED_FONT_CACHE[font_key]
            except KeyError:
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
                except KeyError:
                    try:
                        font_family = FontFamily(self.interface.family)
                    except ArgumentException:
                        print(
                            f"Unknown font '{self.interface}'; "
                            "using system font as a fallback"
                        )
                        font_family = DEFAULT_FONT.FontFamily

            else:
                try:
                    self._pfc = PrivateFontCollection()
                    self._pfc.AddFontFile(font_path)
                    font_family = self._pfc.Families[0]
                except FileNotFoundException:
                    raise ValueError(f"Font file {font_path} could not be found")
                except (IndexError, ExternalException):
                    raise ValueError(f"Unable to load font file {font_path}")

            # Convert font style to Winforms format
            font_style = FontStyle.Regular
            if self.interface.weight.lower() == "bold" and font_family.IsStyleAvailable(
                FontStyle.Bold
            ):
                font_style |= FontStyle.Bold
            if (
                # Winforms doesn't recognize Oblique; so we interpret as Italic
                self.interface.style.lower() in {"italic", "oblique"}
                and font_family.IsStyleAvailable(FontStyle.Italic)
            ):
                font_style |= FontStyle.Italic

            # Convert font size to Winforms format
            if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                font_size = DEFAULT_FONT.Size
            else:
                font_size = self.interface.size

            font = WinFont(font_family, font_size, font_style)
            _FONT_CACHE[self.interface] = font

        self.native = font

    def metric(self, name):
        """Return the given metric, measured in CSS pixels."""
        family = self.native.FontFamily
        style = self.native.Style
        em_height = self.native.SizeInPoints * 96 / 72
        design_unit = em_height / family.GetEmHeight(style)
        return design_unit * getattr(family, f"Get{name}")(style)
