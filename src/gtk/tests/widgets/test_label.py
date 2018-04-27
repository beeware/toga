import unittest
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except ImportError:
    import sys
    # If we're on Linux, Gtk *should* be available. If it isn't, make
    # Gtk an object... but in such a way that every test will fail,
    # because the object isn't actually the Gtk interface.
    if sys.platform == 'linux':
        Gtk = object()
    else:
        Gtk = None

import toga
from toga.constants import MONOSPACE, OBLIQUE, BOLD


def handle_events():
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)


@unittest.skipIf(Gtk is None,
                 "Can't run GTK implementation tests on a non-Linux platform")
class TestGtkLabel(unittest.TestCase):
    def setUp(self):
        self.label = toga.Label('Gtk Test Font')
        self.gtk_label = self.label._impl.native

    def test_can_set_font(self):
        self.label.style.font_family = MONOSPACE
        self.label.style.font_size = 22
        self.label.style.font_style = OBLIQUE
        self.label.style.font_weight = BOLD

        pango_context = self.gtk_label.get_pango_context()
        native_font = pango_context.get_font_description().to_string().lower()

        self.assertIn(MONOSPACE, native_font)
        self.assertIn(str(22), native_font)
        self.assertIn(OBLIQUE, native_font)
        self.assertIn(BOLD, native_font)
