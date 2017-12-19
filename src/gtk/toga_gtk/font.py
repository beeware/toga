import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

try:
    gi.require_version("Pango", "1.0")
    from gi.repository import Pango
except ImportError:
    Pango = None


class Font:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        if Pango is None:
            raise RuntimeError(
                "'from gi.repository import Pango' failed; may need to install gir1.2-pango-1.0."
            )

        self.native = Pango.FontDescription.from_string(
            self.interface.family + " " + str(self.interface.size))

    def measure(self, text, tight):
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


class Measure(Gtk.Widget):
    """Gtk.Widget for Font.measure in order to create a Pango Layout
    """
    def create(self):
        pass
