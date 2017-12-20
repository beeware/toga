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


def native_font(font):
    if Pango is None:
        raise RuntimeError(
            "'from gi.repository import Pango' failed; may need to install gir1.2-pango-1.0."
        )

    try:
        native = _FONT_CACHE[font]
    except KeyError:
        native = Pango.FontDescription.from_string('{font.family} {font.size}'.format(font=font))
        _FONT_CACHE[font] = native

    return native


def measure_text(font, text, tight=False):
    measure_widget = Measure()
    layout = measure_widget.create_pango_layout(text)
    layout.set_font_description(native_font(font))
    ink, logical = layout.get_extents()
    if tight:
        width = ink.width / Pango.SCALE
        height = ink.height / Pango.SCALE
    else:
        width = logical.width / Pango.SCALE
        height = logical.height / Pango.SCALE

    return width, height
