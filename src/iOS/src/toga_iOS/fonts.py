from rubicon.objc import NSMutableDictionary

from toga.fonts import (
    CURSIVE,
    FANTASY,
    MESSAGE,
    MONOSPACE,
    NORMAL,
    SANS_SERIF,
    SERIF,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE
)
from toga_iOS.libs import NSAttributedString, NSFontAttributeName, UIFont

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                # iOS default label size is 17pt
                # FIXME: make this dynamic.
                size = 17
            else:
                size = self.interface.size

            if self.interface.family == SYSTEM:
                font = UIFont.systemFontOfSize(size)
            elif self.interface.family == MESSAGE:
                font = UIFont.messageFontOfSize(size)
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
                font = UIFont.fontWithName(full_name, size=size)

                if font is None:
                    print("Unable to load font: {}pt {}".format(self.interface.size, full_name))
                else:
                    _FONT_CACHE[self.interface] = font

        self.native = font

    def measure(self, text, tight=False):
        textAttributes = NSMutableDictionary.alloc().init()
        textAttributes[NSFontAttributeName] = self.native
        text_string = NSAttributedString.alloc().initWithString_attributes_(text, textAttributes)
        size = text_string.size()

        # TODO: This is a magic fudge factor...
        # Replace the magic with SCIENCE.
        size.width += 3
        return size.width, size.height
