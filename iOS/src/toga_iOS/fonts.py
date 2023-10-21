from pathlib import Path

from fontTools.ttLib import TTFont

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
)
from toga_iOS.libs import (
    NSURL,
    UIFont,
    UIFontDescriptorTraitBold,
    UIFontDescriptorTraitItalic,
)
from toga_iOS.libs.core_text import core_text, kCTFontManagerScopeProcess

_FONT_CACHE = {}
_CUSTOM_FONT_NAMES = {}


class Font:
    def __init__(self, interface):
        self.interface = interface
        try:
            attributed_font = _FONT_CACHE[self.interface]
        except KeyError:
            font_family = self.interface.family
            font_key = self.interface._registered_font_key(
                family=font_family,
                weight=self.interface.weight,
                style=self.interface.style,
                variant=self.interface.variant,
            )

            try:
                # Built in fonts have known names; no need to interrogate a file.
                custom_font_name = {
                    SYSTEM: None,  # No font name required
                    MESSAGE: None,  # No font name required
                    SERIF: "Times-Roman",
                    SANS_SERIF: "Helvetica",
                    CURSIVE: "Snell Roundhand",
                    FANTASY: "Papyrus",
                    MONOSPACE: "Courier New",
                }[font_family]
            except KeyError:
                try:
                    font_path = _REGISTERED_FONT_CACHE[font_key]
                except KeyError:
                    # The requested font has not been registered
                    print(
                        f"Unknown font '{self.interface}'; "
                        "using system font as a fallback"
                    )
                    font_family = SYSTEM
                    custom_font_name = None
                else:
                    # We have a path for a font file.
                    try:
                        # A font *file* an only be registered once under Cocoa.
                        custom_font_name = _CUSTOM_FONT_NAMES[font_path]
                    except KeyError:
                        if Path(font_path).is_file():
                            font_url = NSURL.fileURLWithPath(font_path)
                            success = core_text.CTFontManagerRegisterFontsForURL(
                                font_url, kCTFontManagerScopeProcess, None
                            )
                            if success:
                                ttfont = TTFont(font_path)
                                custom_font_name = ttfont["name"].getBestFullName()
                                # Preserve the Postscript font name contained in the
                                # font file.
                                _CUSTOM_FONT_NAMES[font_path] = custom_font_name
                            else:
                                raise ValueError(
                                    f"Unable to load font file {font_path}"
                                )
                        else:
                            raise ValueError(
                                f"Font file {font_path} could not be found"
                            )

            if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                size = UIFont.labelFontSize
            else:
                # A "point" in Apple APIs is equivalent to a CSS pixel, but the Toga
                # public API works in CSS points, which are slightly larger
                # (https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Explained/Explained.html).
                size = self.interface.size * 96 / 72

            if font_family == SYSTEM:
                font = UIFont.systemFontOfSize(size)
            elif font_family == MESSAGE:
                font = UIFont.systemFontOfSize(size)
            else:
                font = UIFont.fontWithName(custom_font_name, size=size)

            # Convert the base font definition into a font with all the desired traits.
            traits = 0
            if self.interface.weight == BOLD:
                traits |= UIFontDescriptorTraitBold
            if self.interface.style in {ITALIC, OBLIQUE}:
                traits |= UIFontDescriptorTraitItalic

            if traits:
                # If there is no font with the requested traits, this returns None.
                attributed_font = UIFont.fontWithDescriptor(
                    font.fontDescriptor.fontDescriptorWithSymbolicTraits(traits),
                    size=size,
                )
                if attributed_font is None:
                    attributed_font = font
            else:
                attributed_font = font

            _FONT_CACHE[self.interface] = attributed_font.retain()

        self.native = attributed_font
