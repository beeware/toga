import toga
from toga.constants import MONOSPACE, ITALIC, SMALL_CAPS, BOLD
import unittest
import gi

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
except ImportError:
    import sys
    # If we're on Linux, Gtk *should* be available. If it isn't, make
    # Gtk an object... but in such a way that every test will fail,
    # because the object isn't actually the Gtk interface.
    if sys.platform == 'linux':
        Gtk = object()
    else:
        Gtk = None

try:
    gi.require_version("Pango", "1.0")
    from gi.repository import Pango
except ImportError:
    Pango = None


@unittest.skipIf(Pango is None, 'Pango import error')
@unittest.skipIf(Gtk is None,
                 "Can't run GTK implementation tests on a non-Linux platform")
class TestFontImplementation(unittest.TestCase):
    def setUp(self):
        self.font_choices = {
            'family': MONOSPACE,
            'size': 22,
            'style': ITALIC,
            'variant': SMALL_CAPS,
            'weight': BOLD
        }

        self.font = toga.Font(
            family=self.font_choices['family'],
            size=self.font_choices['size'],
            style=self.font_choices['style'],
            variant=self.font_choices['variant'],
            weight=self.font_choices['weight'])

        self.pango_font = self.font._impl.native

        self.font_desc_str = self.pango_font.to_string().lower().split(' ')

    def tearDown(self):
        self.pango_font.free()

    def test_font_size(self):
        # int to str
        self.assertIn(str(self.font_choices['size']), self.font_desc_str)

    def test_font_family(self):
        self.assertIn(self.font_choices['family'], self.font_desc_str)

    def test_font_style(self):
        self.assertIn(self.font_choices['style'], self.font_desc_str)

    def test_font_variant(self):
        self.assertIn(self.font_choices['variant'], self.font_desc_str)

    def test_font_weight(self):
        self.assertIn(self.font_choices['weight'], self.font_desc_str)


if __name__ == '__main__':
    unittest.main()
