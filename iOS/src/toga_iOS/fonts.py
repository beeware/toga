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
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    UnknownFontError,
)
from toga_iOS.libs import (
    NSURL,
    UIFont,
    UIFontDescriptorTraitBold,
    UIFontDescriptorTraitItalic,
)
from toga_iOS.libs.core_text import core_text, kCTFontManagerScopeProcess

_CUSTOM_FONT_NAMES = {}


class Font:
    def __init__(self, interface):
        self.interface = interface

    def load_predefined_system_font(self):
        """Use one of the system font names Toga predefines."""
        try:
            # Built in fonts have known names; no need to interrogate a file.
            font_name = {
                SYSTEM: SYSTEM,
                MESSAGE: SYSTEM,  # No separate "message" font on iOS
                SERIF: "Times-Roman",
                SANS_SERIF: "Helvetica",
                CURSIVE: "Snell Roundhand",
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
            # A font *file* an only be registered once under iOS, so check if it's
            # already registered.
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
        raise UnknownFontError("Arbitrary system fonts not yet supported on iOS")

    def _assign_native(self, font_name):
        if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
            size = UIFont.labelFontSize
        else:
            # A "point" in Apple APIs is equivalent to a CSS pixel, but the Toga
            # public API works in CSS points, which are slightly larger
            # (https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Explained/Explained.html).
            size = self.interface.size * 96 / 72

        # Construct the UIFont
        if font_name == SYSTEM:
            font = UIFont.systemFontOfSize(size)
        else:
            font = UIFont.fontWithName(font_name, size=size)

        # Convert the base font definition into a font with all the desired traits.
        traits = 0
        if self.interface.weight == BOLD:
            traits |= UIFontDescriptorTraitBold
        if self.interface.style in {ITALIC, OBLIQUE}:
            traits |= UIFontDescriptorTraitItalic

        if traits:
            # If there is no font with the requested traits, this returns None.
            font_with_traits = UIFont.fontWithDescriptor(
                font.fontDescriptor.fontDescriptorWithSymbolicTraits(traits),
                size=size,
            )
            font = font_with_traits or font

        self.native = font
        _IMPL_CACHE[self.interface] = self
