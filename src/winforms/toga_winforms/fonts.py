from .libs import FontFamily, FontStyle, Single, WinFont, WinForms, win_font_family
from .libs.fonts import win_font_size, win_font_style
from .libs.winforms import PrivateFontCollection
from toga.fonts import _REGISTERED_FONT_CACHE

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
            font_key = self.interface.make_registered_font_key(
                self.interface.family,
                weight=self.interface.weight,
                style=self.interface.style,
                variant=self.interface.variant,
            )
            if font_key in _REGISTERED_FONT_CACHE:
                try:
                    self._pfc = PrivateFontCollection()
                    self._pfc.AddFontFile(
                        str(
                            self.interface.factory.paths.app
                            / _REGISTERED_FONT_CACHE[font_key]
                        )
                    )
                    font_size = win_font_size(self.interface.size)
                    font_style = win_font_style(
                        self.interface.weight,
                        self.interface.style,
                        self._pfc.Families[0],
                    )
                    font = WinFont(self._pfc.Families[0], float(font_size), font_style)
                except Exception as ex:
                    print(
                        "Registered font with the key '"
                        + str(font_key)
                        + "' could not be loaded: "
                        + str(ex)
                    )
            if font is None:
                font_family = win_font_family(self.interface.family)
                font_style = win_font_style(
                    self.interface.weight, self.interface.style, font_family
                )
                font_size = win_font_size(self.interface.size)
                font = WinFont.Overloads[FontFamily, Single, FontStyle](
                    font_family, font_size, font_style
                )
            _FONT_CACHE[self.interface] = font

        self.native = font

    def measure(self, text, dpi, tight=False):
        size = WinForms.TextRenderer.MeasureText(text, self.native)
        return (
            points_to_pixels(size.Width, dpi),
            points_to_pixels(size.Height, dpi),
        )
