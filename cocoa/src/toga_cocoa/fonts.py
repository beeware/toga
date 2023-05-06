from toga.fonts import (
    _REGISTERED_FONT_CACHE,
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
    NSURL,
    NSAttributedString,
    NSFont,
    NSFontAttributeName,
    NSFontManager,
    NSFontMask,
    NSMutableDictionary,
)
from toga_cocoa.libs.core_text import core_text, kCTFontManagerScopeProcess

_FONT_CACHE = {}
_POSTSCRIPT_NAMES = {
    SERIF: "Times-Roman",
    SANS_SERIF: "Helvetica",
    CURSIVE: "Apple Chancery",
    FANTASY: "Papyrus",
    MONOSPACE: "Courier New",
}


class Font:
    def __init__(self, interface):
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            font = None
            family = self.interface.family
            font_key = self.interface.registered_font_key(
                family,
                weight=self.interface.weight,
                style=self.interface.style,
                variant=self.interface.variant,
            )

            # Default system font size on Cocoa is 12pt
            if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                font_size = NSFont.systemFontSize
            else:
                font_size = self.interface.size

            if font_key in _REGISTERED_FONT_CACHE:
                # print("LOAD", font_key, _REGISTERED_FONT_CACHE[font_key])
                font_path = str(
                    self.interface.factory.paths.app / _REGISTERED_FONT_CACHE[font_key]
                )

                font_url = NSURL.fileURLWithPath(font_path)
                success = core_text.CTFontManagerRegisterFontsForURL(
                    font_url, kCTFontManagerScopeProcess, None
                )
                if success:
                    # FIXME - this naming needs to be dynamically determined from the font,
                    # rather than hard-coded
                    _POSTSCRIPT_NAMES[family] = {
                        "awesome-free-solid": "Font Awesome 5 Free",
                        "Endor": "ENDOR",
                    }.get(family, family)

            if family == SYSTEM:
                font = NSFont.systemFontOfSize(font_size)
            elif family == MESSAGE:
                font = NSFont.messageFontOfSize(font_size)
            else:
                try:
                    font = NSFont.fontWithName(
                        _POSTSCRIPT_NAMES[family], size=font_size
                    )
                except KeyError:
                    pass

            if font is None:
                print(
                    f"Unknown font '{self.interface}'; "
                    "using system font as a fallback"
                )
                font = NSFont.systemFontOfSize(font_size)

            # Convert the base font definition into a font with all the desired traits.
            attributes_mask = 0
            if self.interface.weight == BOLD:
                attributes_mask |= NSFontMask.Bold.value

            if self.interface.style == ITALIC:
                attributes_mask |= NSFontMask.Italic.value
            elif self.interface.style == SMALL_CAPS:
                attributes_mask |= NSFontMask.SmallCaps.value

            if attributes_mask:
                attributed_font = NSFontManager.sharedFontManager.convertFont(
                    font, toHaveTrait=attributes_mask
                )
                # print(font, attributed_font)
            else:
                attributed_font = font

            full_name = "{family}{weight}{style}".format(
                family=family,
                weight=(" " + self.interface.weight.title())
                if self.interface.weight is not NORMAL
                else "",
                style=(" " + self.interface.style.title())
                if self.interface.style is not NORMAL
                else "",
            )

            if attributed_font is None:
                print(
                    "Unable to load font: {}pt {}".format(
                        self.interface.size, full_name
                    )
                )
            else:
                font = attributed_font

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
