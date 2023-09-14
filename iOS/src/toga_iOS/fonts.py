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
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    SYSTEM_DEFAULT_FONTS,
)
from toga_iOS.libs import (
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
            font_key = self.interface._registered_font_key(
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

            if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                # iOS default label size is 17pt
                # FIXME: make this dynamic.
                size = 17
            else:
                size = self.interface.size

            if self.interface.family == SYSTEM:
                base_font = UIFont.systemFontOfSize(size)
            elif self.interface.family == MESSAGE:
                base_font = UIFont.systemFontOfSize(size)
            else:
                family = {
                    SERIF: "Times-Roman",
                    SANS_SERIF: "Helvetica",
                    CURSIVE: "Snell Roundhand",
                    FANTASY: "Papyrus",
                    MONOSPACE: "Courier New",
                }.get(self.interface.family, self.interface.family)

                base_font = UIFont.fontWithName(family, size=size)
                if base_font is None:
                    print(f"Unable to load font: {size}pt {family}")
                    base_font = UIFont.systemFontOfSize(size)

            # Convert the base font definition into a font with all the desired traits.
            traits = 0
            if self.interface.weight == BOLD:
                traits |= UIFontDescriptorTraitBold
            if self.interface.style in {ITALIC, OBLIQUE}:
                traits |= UIFontDescriptorTraitItalic

            if traits:
                # If there is no font with the requested traits, this returns the original
                # font unchanged.
                font = UIFont.fontWithDescriptor(
                    base_font.fontDescriptor.fontDescriptorWithSymbolicTraits(traits),
                    size=size,
                )
                # If the traits conversion failed, fall back to the default font.
                if font is None:
                    font = base_font
            else:
                font = base_font

            _FONT_CACHE[self.interface] = font.retain()

        self.native = font
