from pathlib import Path
from warnings import warn

from toga.fonts import (
    _IMPL_CACHE,
    _REGISTERED_FONT_CACHE,
    BOLD,
    ITALIC,
    OBLIQUE,
    SMALL_CAPS,
    SYSTEM_DEFAULT_FONT_SIZE,
    SYSTEM_DEFAULT_FONTS,
    UnknownFontError,
)

from .libs import FontConfig, Pango, PangoCairo, PangoFc

IMPORT_ERROR = (
    "Unable to import {}. Have you installed the corresponding system packages and "
    "GIRepository introspection typelib files?"
)


class Font:
    def __init__(self, interface):
        self.interface = interface

        # Can't meaningfully get test coverage for pango not being installed
        if Pango is None:  # pragma: no cover
            raise RuntimeError(IMPORT_ERROR.format("Pango"))
        if PangoCairo is None:  # pragma: no cover
            raise RuntimeError(IMPORT_ERROR.format("PangoCairo"))

    def load_predefined_system_font(self):
        """Use one of the system font names Toga predefines."""
        if self.interface.family not in SYSTEM_DEFAULT_FONTS:
            raise UnknownFontError(f"{self.interface} not a predefined system font")

        self._assign_native()

    def load_user_registered_font(self):
        """Use a font that the user has registered in their code."""
        font_key = self.interface._registered_font_key(
            self.interface.family,
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
        if not Path(font_path).is_file():
            raise ValueError(f"Font file {font_path} could not be found")

        success = FontConfig.add_font_file(font_path)
        if not success:
            raise ValueError(f"Unable to load font file {font_path}")

        # PangoFc provides the base class of the default font map, so if its typelib
        # file is missing, the cache_clear method will not be visible.
        if PangoFc is None:  # pragma: no cover
            # Debian Buster doesn't include the typelib file in any package, but it
            # works even without a cache_clear, so continue with a warning.
            warn(IMPORT_ERROR.format("PangoFc"), stacklevel=2)
        else:
            # Ubuntu 22.04 includes the typelib file in gir1.2-pango-1.0, and it does
            # require a cache_clear to make new fonts visible to the Canvas.
            PangoCairo.FontMap.get_default().cache_clear()

        self._assign_native()

    def load_arbitrary_system_font(self):
        # Check for a font installed on the system.
        installed = PangoCairo.FontMap.get_default().get_family(self.interface.family)
        if installed is None:
            raise UnknownFontError(f"{self.interface} not found installed on system")

        self._assign_native()

    def _assign_native(self):
        # Initialize font with properties '[Font family] NORMAL NORMAL NORMAL 0'
        font = Pango.FontDescription(self.interface.family)

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

        self.native = font
        _IMPL_CACHE[self.interface] = self
