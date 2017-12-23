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
            font = Pango.FontDescription.from_string('{font.family} {font.size}'.format(font=self.interface))
            _FONT_CACHE[font] = font

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
