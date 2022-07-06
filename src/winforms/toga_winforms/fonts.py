from toga.fonts import _REGISTERED_FONT_CACHE

from toga_winforms.libs import (
    WinFont,
    WinForms,
    win_font_family
)
from toga_winforms.libs.fonts import win_font_size, win_font_style
from toga_winforms.libs.winforms import (
    ExternalException,
    FileNotFoundException,
    PrivateFontCollection
)

_FONT_CACHE = {}


def points_to_pixels(points, dpi):
    return points * 72 / dpi


class Font:
    def __init__(self, interface):
        self._pfc = None  # this needs to be a instance variable, otherwise we might get Winforms exceptions later
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
                try:
                    self._pfc = PrivateFontCollection()
                    self._pfc.AddFontFile(font_path)
                    font_family = self._pfc.Families[0]
                except FileNotFoundException as e:
                    print(f"Registered font path {font_path!r} could not be found: {e}")
                except ExternalException as e:
                    print(f"Registered font path {font_path!r} could not be loaded: {e}")
                except IndexError as e:
                    print(f"Registered font {font_key} could not be loaded: {e}")
            except KeyError:
                font_family = win_font_family(self.interface.family)

            font_style = win_font_style(
                self.interface.weight,
                self.interface.style,
                font_family,
            )
            font_size = win_font_size(self.interface.size)
            font = WinFont(font_family, font_size, font_style)
            _FONT_CACHE[self.interface] = font

        self.native = font

    def measure(self, text, dpi, tight=False):
        size = WinForms.TextRenderer.MeasureText(text, self.native)
        return (
            points_to_pixels(size.Width, dpi),
            points_to_pixels(size.Height, dpi),
        )
