from pathlib import Path

from toga.fonts import (
    _REGISTERED_FONT_CACHE,
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    OBLIQUE,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    SYSTEM_DEFAULT_FONTS,
)
from toga_cocoa.libs import (
    NSFont,
    NSFontManager,
    NSFontMask,
)

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface
        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            font_key = self.interface.registered_font_key(
                self.interface.family,
                weight=self.interface.weight,
                style=self.interface.style,
                variant=self.interface.variant,
            )
            try:
                font_path = _REGISTERED_FONT_CACHE[font_key]
            except KeyError:
                # Not a pre-registered font
                if self.interface.family not in SYSTEM_DEFAULT_FONTS:
                    print(
                        f"Unknown font '{self.interface}'; "
                        "using system font as a fallback"
                    )
            else:
                if Path(font_path).is_file():
                    # TODO: Load font file
                    self.interface.factory.not_implemented("Custom font loading")
                    # if corrupted font file:
                    #     raise ValueError(f"Unable to load font file {font_path}")
                else:
                    raise ValueError(f"Font file {font_path} could not be found")

            # Default system font size on Cocoa is 12pt
            if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                font_size = NSFont.systemFontSize
            else:
                font_size = self.interface.size

            if self.interface.family == SYSTEM:
                font = NSFont.systemFontOfSize(font_size)
            elif self.interface.family == MESSAGE:
                font = NSFont.messageFontOfSize(font_size)
            else:
                family = {
                    SERIF: "Times-Roman",
                    SANS_SERIF: "Helvetica",
                    CURSIVE: "Apple Chancery",
                    FANTASY: "Papyrus",
                    MONOSPACE: "Courier New",
                }.get(self.interface.family, self.interface.family)

                font = NSFont.fontWithName(family, size=self.interface.size)

                if font is None:
                    print(
                        "Unable to load font: {}pt {}".format(
                            self.interface.size, family
                        )
                    )
                    font = NSFont.systemFontOfSize(font_size)

            # Convert the base font definition into a font with all the desired traits.
            attributes_mask = 0
            if self.interface.weight == BOLD:
                attributes_mask |= NSFontMask.Bold.value
            if self.interface.style in {ITALIC, OBLIQUE}:
                # Oblique is the fallback for Italic.
                attributes_mask |= NSFontMask.Italic.value
            if self.interface.variant == SMALL_CAPS:
                attributes_mask |= NSFontMask.SmallCaps.value
            if attributes_mask:
                # If there is no font with the requested traits, this returns the original
                # font unchanged.
                font = NSFontManager.sharedFontManager.convertFont(
                    font, toHaveTrait=attributes_mask
                )

            _FONT_CACHE[self.interface] = font.retain()

        self.native = font
