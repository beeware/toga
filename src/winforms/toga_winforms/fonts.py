from .libs import WinFont, WinForms
from .libs import FontFamily, FontStyle, Single, win_font_family
from .libs.fonts import win_font_style

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            font_family = win_font_family(self.interface.family)
            font_style = win_font_style(
                self.interface.weight,
                self.interface.style,
                font_family)
            font = WinFont.Overloads[FontFamily, Single, FontStyle](
                font_family, self.interface.size, font_style
            )
            _FONT_CACHE[self.interface] = font

        self.native = font

    def measure(self, text, tight=False):
        size = WinForms.TextRenderer.MeasureText(text, self.native)
        return size.Width, size.Height
