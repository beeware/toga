from toga.fonts import (
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    NORMAL,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)
from toga_cocoa.libs import (
    NSAttributedString,
    NSFont,
    NSFontAttributeName,
    NSFontManager,
    NSFontMask,
    NSMutableDictionary,
)

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            # Default system font size on Cocoa is 12pt
            if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                font_size = NSFont.systemFontSize
            else:
                font_size = self.interface.size

            if self.interface.family == SYSTEM:
                if self.interface.weight == BOLD:
                    font = NSFont.boldSystemFontOfSize(font_size)
                else:
                    font = NSFont.systemFontOfSize(font_size)
            elif self.interface.family == MESSAGE:
                font = NSFont.messageFontOfSize(font_size)
            else:
                if self.interface.family is SERIF:
                    family = "Times-Roman"
                elif self.interface.family is SANS_SERIF:
                    family = "Helvetica"
                elif self.interface.family is CURSIVE:
                    family = "Apple Chancery"
                elif self.interface.family is FANTASY:
                    family = "Papyrus"
                elif self.interface.family is MONOSPACE:
                    family = "Courier New"
                else:
                    family = self.interface.family

                font = NSFont.fontWithName(family, size=self.interface.size)

                if font is None:
                    print(
                        "Unable to load font: {}pt {}".format(
                            self.interface.size, family
                        )
                    )

                # Convert the base font definition into a font with all the desired traits.
                attributes_mask = 0
                if self.interface.weight == BOLD:
                    attributes_mask |= NSFontMask.Bold.value

                if self.interface.style == ITALIC:
                    attributes_mask |= NSFontMask.Italic.value
                elif self.interface.style == SMALL_CAPS:
                    attributes_mask |= NSFontMask.SmallCaps.value

                if attributes_mask:
                    font = NSFontManager.sharedFontManager.convertFont(
                        font, toHaveTrait=attributes_mask
                    )

                full_name = "{family}{weight}{style}".format(
                    family=family,
                    weight=(" " + self.interface.weight.title())
                    if self.interface.weight is not NORMAL
                    else "",
                    style=(" " + self.interface.style.title())
                    if self.interface.style is not NORMAL
                    else "",
                )

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
        text_string = NSAttributedString.alloc().initWithString(
            text, attributes=textAttributes
        )
        size = text_string.size()

        # TODO: This is a magic fudge factor...
        # Replace the magic with SCIENCE.
        size.width += 3
        return size.width, size.height
