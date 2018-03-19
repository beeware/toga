from toga.constants import ITALIC, OBLIQUE, SMALL_CAPS, BOLD
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

try:
    gi.require_version("Pango", "1.0")
    from gi.repository import Pango
except ImportError:
    Pango = None

_FONT_CACHE = {}


class Measure(Gtk.Widget):
    """Gtk.Widget for Font.measure in order to create a Pango Layout
    """

    def create(self):
        pass


class Font:
    def __init__(self, interface):
        self.interface = interface

        if Pango is None:
            raise RuntimeError(
                "'from gi.repository import Pango' failed; may need to install gir1.2-pango-1.0."
            )

        try:
            font = _FONT_CACHE[self.interface]
        except KeyError:

            # Initialize font with properties 'None NORMAL NORMAL NORMAL 0'
            font = Pango.FontDescription()

            # Set font family
            # TODO: Check whether font is installed in system
            font.set_family(self.interface.family)

            # Set font size
            font.set_size(self.interface.size)

            # Set font style
            if self.interface.style is ITALIC:
                font.set_style(Pango.Style.ITALIC)
            elif self.interface.style is OBLIQUE:
                font.set_style(Pango.Style.OBLIQUE)

            # Set font variant
            if self.interface.variant is SMALL_CAPS:
                font.set_variant(Pango.Variant.SMALL_CAPS)

            # Set font weight
            if self.interface.weight is BOLD:
                font.set_weight(Pango.Weight.BOLD)

            _FONT_CACHE[self.interface] = font

        self.native = font

    def measure(self, text, tight=False):
        measure_widget = Measure()
        layout = measure_widget.create_pango_layout(text)
        layout.set_font_description(self.native)
        ink, logical = layout.get_extents()
        if tight:
            width = ink.width / Pango.SCALE
            height = ink.height / Pango.SCALE
        else:
            width = logical.width / Pango.SCALE
            height = logical.height / Pango.SCALE

        return width, height
