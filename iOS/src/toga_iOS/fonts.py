from rubicon.objc import NSMutableDictionary

from toga.fonts import (
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    SANS_SERIF,
    SERIF,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)
from toga_iOS.libs import (
    NSAttributedString,
    NSFontAttributeName,
    UIFont,
    UIFontDescriptorTraitBold,
    UIFontDescriptorTraitItalic,
)

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

                font = UIFont.fontWithName(family, size=size)
                if font is None:
                    print(f"Unable to load font: {size}pt {family}")
                    font = UIFont.systemFontOfSize(size)

            # Convert the base font definition into a font with all the desired traits.
            traits = 0
            if self.interface.weight == BOLD:
                traits |= UIFontDescriptorTraitBold
            if self.interface.style == ITALIC:
                traits |= UIFontDescriptorTraitItalic
            if traits:
                # If there is no font with the requested traits, this returns the original
                # font unchanged.
                font = UIFont.fontWithDescriptor(
                    font.fontDescriptor.fontDescriptorWithSymbolicTraits(traits),
                    size=size,
                )

            _FONT_CACHE[self.interface] = font.retain()

        self.native = font

    def measure(self, text, tight=False):
        textAttributes = NSMutableDictionary.alloc().init()
        textAttributes[NSFontAttributeName] = self.native
        text_string = NSAttributedString.alloc().initWithString_attributes_(
            text, textAttributes
        )
        size = text_string.size()

        # TODO: This is a magic fudge factor...
        # Replace the magic with SCIENCE.
        size.width += 3
        return size.width, size.height
