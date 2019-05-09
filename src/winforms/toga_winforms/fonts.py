from .libs import WinFont
from .libs import FontFamily, FontStyle, Single, win_font_family

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            font_family = win_font_family(self.interface.family)
            font_style = FontStyle.Regular
            if self.interface.weight.lower() == "bold" and font_family.IsStyleAvailable(FontStyle.Bold):
                font_style += FontStyle.Bold
            if self.interface.style.lower() == "italic" and font_family.IsStyleAvailable(FontStyle.Italic):
                font_style += FontStyle.Italic
            font = WinFont.Overloads[FontFamily, Single, FontStyle](
                font_family, self.interface.size, font_style
            )
            _FONT_CACHE[self.interface] = font

        self.native = font
