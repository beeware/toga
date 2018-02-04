from rubicon.objc import NSDictionary, NSSize, send_super, objc_method
from .libs import NSString, NSFont, NSFontAttributeName
from toga.font import MESSAGE, NORMAL, SYSTEM, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            if self.interface.family == SYSTEM:
                font = NSFont.systemFontOfSize(self.interface.size)
            elif self.interface.family == MESSAGE:
                font = NSFont.messageFontOfSize(self.interface.size)
            else:
                if self.interface.family is SERIF:
                    family = 'Times-Roman'
                elif self.interface.family is SANS_SERIF:
                    family = 'Helvetica'
                elif self.interface.family is CURSIVE:
                    family = 'Apple Chancery'
                elif self.interface.family is FANTASY:
                    family = 'Papyrus'
                elif self.interface.family is MONOSPACE:
                    family = 'Courier New'
                else:
                    family = self.interface.family

                full_name = '{family}{weight}{style}'.format(
                    family=family,
                    weight=(' ' + self.interface.weight.title()) if self.interface.weight is not NORMAL else '',
                    style=(' ' + self.interface.style.title()) if self.interface.style is not NORMAL else '',
                )
                font = NSFont.fontWithName(full_name, size=self.interface.size)

                if font is None:
                    print("Unable to load font: {}pt {}".format(self.interface.size, full_name))
                else:
                    _FONT_CACHE[self.interface] = font

        self.native = font

    def measure(self, text, tight=False):
        font_attrs = {self.native: NSFontAttributeName}
        print(font_attrs)
        text_string = TextString(text)
        print(text_string)
        [width, height] = text_string.sizeWithAttributes(font_attrs)
        return width, height


class TextString(NSString):
    @objc_method
    def sizeWithAttributes(self, attrs: NSDictionary) -> NSSize:
        size = send_super(
            self, 'sizeWithAttributes:', attrs, restype=NSSize, argtypes=[NSDictionary]
        )

        return size
