from toga.fonts import (
    MESSAGE,
    NORMAL, BOLD,
    SYSTEM,
    SERIF,
    SANS_SERIF,
    CURSIVE,
    FANTASY,
    MONOSPACE,
)

from toga_cocoa.libs import NSAttributedString, NSFont, NSFontAttributeName, NSMutableDictionary

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            if self.interface.family == SYSTEM:
                if self.interface.weight == BOLD:
                    font = NSFont.boldSystemFontOfSize(self.interface.size)
                else:
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
                    print(
                        "Unable to load font: {}pt {}".format(
                            self.interface.size, full_name
                        )
                    )
                else:
                    _FONT_CACHE[self.interface] = font

        self.native = font

    def measure(self, text, tight=False):
        textAttributes = NSMutableDictionary.alloc().init()
        textAttributes[NSFontAttributeName] = self.native
        text_string = NSAttributedString.alloc().initWithString_attributes_(text, textAttributes)
        size = text_string.size()
        size.width += 3
        return size.width, size.height
