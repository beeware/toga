from pathlib import Path

from toga.fonts import (
    _REGISTERED_FONT_CACHE,
    BOLD,
    ITALIC,
    OBLIQUE,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    SYSTEM_DEFAULT_FONTS,
)

from .libs import FontConfig, Pango

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface

        # Can't meaningfully get test coverage for pango not being installed
        if Pango is None:  # pragma: no cover
            raise RuntimeError(
                "Unable to import Pango. Have you installed the Pango and gobject-introspection system libraries?"
            )

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
                    FontConfig.add_font_file(font_path)
                else:
                    raise ValueError(f"Font file {font_path} could not be found")

            # Initialize font with properties 'None NORMAL NORMAL NORMAL 0'
            font = Pango.FontDescription()

            family = self.interface.family
            if family != SYSTEM:
                family = f"{family}, {SYSTEM}"  # Default to system

            font.set_family(family)

            # If this is a non-default font size, set the font size
            if self.interface.size != SYSTEM_DEFAULT_FONT_SIZE:
                font.set_size(self.interface.size * Pango.SCALE)

            # Set font style
            if self.interface.style == ITALIC:
                font.set_style(Pango.Style.ITALIC)
            elif self.interface.style == OBLIQUE:
                font.set_style(Pango.Style.OBLIQUE)

            # Set font variant
            if self.interface.variant == SMALL_CAPS:
                font.set_variant(Pango.Variant.SMALL_CAPS)

            # Set font weight
            if self.interface.weight == BOLD:
                font.set_weight(Pango.Weight.BOLD)

            _FONT_CACHE[self.interface] = font

        self.native = font
