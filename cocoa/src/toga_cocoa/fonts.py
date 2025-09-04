from pathlib import Path

from fontTools.ttLib import TTFont

from toga.fonts import (
    _IMPL_CACHE,
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
    UnknownFontError,
)
from toga_cocoa.libs import (
    NSURL,
    NSFont,
    NSFontManager,
    NSFontMask,
)
from toga_cocoa.libs.core_text import core_text, kCTFontManagerScopeProcess

_CUSTOM_FONT_NAMES = {}


class Font:
    def __init__(self, interface):
        self.interface = interface

    def load_predefined_system_font(self):
        """Use one of the system font names Toga predefines."""
        try:
            # Built-in fonts have known names; no need to interrogate a file.
            font_name = {
                SYSTEM: SYSTEM,
                MESSAGE: MESSAGE,
                SERIF: "Times-Roman",
                SANS_SERIF: "Helvetica",
                CURSIVE: "Apple Chancery",
                FANTASY: "Papyrus",
                MONOSPACE: "Courier New",
            }[self.interface.family]

        except KeyError as exc:
            msg = f"{self.interface} not a predefined system font"
            raise UnknownFontError(msg) from exc

        self._assign_native(font_name)

    def load_user_registered_font(self):
        """Use a font that the user has registered in their code."""
        font_key = self.interface._registered_font_key(
            family=self.interface.family,
            weight=self.interface.weight,
            style=self.interface.style,
            variant=self.interface.variant,
        )
        try:
            font_path = _REGISTERED_FONT_CACHE[font_key]
        except KeyError as exc:
            msg = f"{self.interface} not a user-registered font"
            raise UnknownFontError(msg) from exc

        # Yes, user has registered this font.
        try:
            # A font *file* can only be registered once under Cocoa, so
            # check if it's already registered.
            font_name = _CUSTOM_FONT_NAMES[font_path]

        except KeyError as exc:
            # Attempt to register the font file.
            if not Path(font_path).is_file():
                msg = f"Font file {font_path} could not be found"
                raise ValueError(msg) from exc

            font_url = NSURL.fileURLWithPath(font_path)
            success = core_text.CTFontManagerRegisterFontsForURL(
                font_url, kCTFontManagerScopeProcess, None
            )
            if not success:
                msg = f"Unable to load font file {font_path}"
                raise ValueError(msg) from exc

            ttfont = TTFont(font_path)
            # Preserve the Postscript font name contained in the
            # font file.
            font_name = ttfont["name"].getBestFullName()
            _CUSTOM_FONT_NAMES[font_path] = font_name

        self._assign_native(font_name)

    def load_arbitrary_system_font(self):
        """Use a font available on the system."""
        raise UnknownFontError("Arbitrary system fonts not yet supported on macOS")

    def _assign_native(self, font_name):
        if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
            size = NSFont.systemFontSize
        else:
            # A "point" in Apple APIs is equivalent to a CSS pixel, but the Toga public
            # API works in CSS points, which are slightly larger
            # (https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Explained/Explained.html).
            size = self.interface.size * 96 / 72

        # Construct the NSFont
        if font_name == SYSTEM:
            font = NSFont.systemFontOfSize(size)
        elif font_name == MESSAGE:
            font = NSFont.messageFontOfSize(size)
        else:
            font = NSFont.fontWithName(font_name, size=size)

        # Convert the base font definition into a font with all the desired traits.
        traits = 0
        if self.interface.weight == BOLD:
            traits |= NSFontMask.Bold.value
        if self.interface.style in {ITALIC, OBLIQUE}:
            traits |= NSFontMask.Italic.value
        if self.interface.variant == SMALL_CAPS:
            traits |= NSFontMask.SmallCaps.value

        if traits:
            font = NSFontManager.sharedFontManager.convertFont(font, toHaveTrait=traits)

        self.native = font
        _IMPL_CACHE[self.interface] = self
