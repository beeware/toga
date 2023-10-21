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
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)
from toga_cocoa.libs import (
    NSURL,
    NSFont,
    NSFontManager,
    NSFontMask,
)
from toga_cocoa.libs.core_text import core_text, kCTFontManagerScopeProcess

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
                    CURSIVE: "Apple Chancery",
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
                font_size = NSFont.systemFontSize
            else:
                # A "point" in Apple APIs is equivalent to a CSS pixel, but the Toga
                # public API works in CSS points, which are slightly larger
                # (https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Explained/Explained.html).
                font_size = self.interface.size * 96 / 72

            # Construct the NSFont
            if font_family == SYSTEM:
                font = NSFont.systemFontOfSize(font_size)
            elif font_family == MESSAGE:
                font = NSFont.messageFontOfSize(font_size)
            else:
                font = NSFont.fontWithName(custom_font_name, size=font_size)

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
                attributed_font = NSFontManager.sharedFontManager.convertFont(
                    font, toHaveTrait=attributes_mask
                )
            else:
                attributed_font = font

            _FONT_CACHE[self.interface] = attributed_font.retain()

        self.native = attributed_font
