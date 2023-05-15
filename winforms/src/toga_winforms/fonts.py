from toga.fonts import _REGISTERED_FONT_CACHE
from toga_winforms.libs import WinFont, win_font_family
from toga_winforms.libs.fonts import win_font_size, win_font_style
from toga_winforms.libs.winforms import (
    ExternalException,
    FileNotFoundException,
    PrivateFontCollection,
)

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self._pfc = None  # this needs to be an instance variable, otherwise we might get Winforms exceptions later
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            font = None
            font_key = self.interface.registered_font_key(
                self.interface.family,
                weight=self.interface.weight,
                style=self.interface.style,
                variant=self.interface.variant,
            )
            try:
                font_path = str(
                    self.interface.factory.paths.app / _REGISTERED_FONT_CACHE[font_key]
                )
            except KeyError:
                font_family = win_font_family(self.interface.family)
            else:
                try:
                    self._pfc = PrivateFontCollection()
                    self._pfc.AddFontFile(font_path)
                    font_family = self._pfc.Families[0]
                except FileNotFoundException:
                    raise ValueError(f"Font file {font_path} could not be found")
                except (IndexError, ExternalException):
                    raise ValueError(f"Unable to load font file {font_path}")

            font_style = win_font_style(
                self.interface.weight,
                self.interface.style,
                font_family,
            )
            font_size = win_font_size(self.interface.size)
            font = WinFont(font_family, font_size, font_style)
            _FONT_CACHE[self.interface] = font

        self.native = font
