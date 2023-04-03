from toga.constants import (
    BOLD,
    ITALIC,
    OBLIQUE,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)

from .libs import Pango

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface

        if Pango is None:
            raise RuntimeError(
                "'from gi.repository import Pango' failed; you may need to install gir1.2-pango-1.0."
            )

        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:
            # Initialize font with properties 'None NORMAL NORMAL NORMAL 0'
            font = Pango.FontDescription()

            # Set font family
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

    def measure(self, text, widget, tight=False):
        layout = widget.create_pango_layout(text)

        layout.set_font_description(self.native)
        ink, logical = layout.get_extents()
        if tight:
            width = (ink.width / Pango.SCALE) - (ink.width * 0.2) / Pango.SCALE
            height = ink.height / Pango.SCALE
        else:
            width = (logical.width / Pango.SCALE) - (logical.width * 0.2) / Pango.SCALE
            height = logical.height / Pango.SCALE

        return width, height
