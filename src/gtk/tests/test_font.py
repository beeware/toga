import unittest

import toga
from toga.constants import ITALIC, OBLIQUE, SMALL_CAPS, BOLD, SYSTEM, CURSIVE
from toga_gtk import fonts as gtk_fonts

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
        self.interface = None
        self.native = None
        self.font_family = SYSTEM
        self.font_size = 12

    def tearDown(self):
        if self.native:  # Avoids 'free'ing invalid pointer
            self.native.free()

    def test_font_default_has_all_attr_set(self):
        self.interface = toga.Font(self.font_family, self.font_size)
        self.native = self.interface._impl.native
        self.assertEqual(self.native.get_family(), SYSTEM)
        self.assertEqual(self.native.get_size() / Pango.SCALE, self.font_size)
        self.assertEqual(self.native.get_style(), Pango.Style.NORMAL)
        self.assertEqual(self.native.get_variant(), Pango.Variant.NORMAL)
        self.assertEqual(self.native.get_weight(), Pango.Weight.NORMAL)

    def test_font_size(self):
        self.font_size = 22
        self.interface = toga.Font(self.font_family, self.font_size)
        self.native = self.interface._impl.native
        self.assertEqual(self.native.get_size() / Pango.SCALE, self.font_size)

    def test_font_style_italic(self):
        self.interface = toga.Font(
            self.font_family, self.font_size, style=ITALIC)
        self.native = self.interface._impl.native
        self.assertEqual(self.native.get_style(), Pango.Style.ITALIC)

    def test_font_style_oblique(self):
        self.interface = toga.Font(
            self.font_family, self.font_size, style=OBLIQUE)
        self.native = self.interface._impl.native
        self.assertEqual(self.native.get_style(), Pango.Style.OBLIQUE)

    def test_font_variant_small_caps(self):
        self.interface = toga.Font(
            self.font_family, self.font_size, variant=SMALL_CAPS)
        self.native = self.interface._impl.native
        self.assertEqual(self.native.get_variant(), Pango.Variant.SMALL_CAPS)

    def test_font_weight_bold(self):
        self.interface = toga.Font(
            self.font_family, self.font_size, weight=BOLD)
        self.native = self.interface._impl.native
        self.assertEqual(self.native.get_weight(), Pango.Weight.BOLD)

    def test_font_cache(self):
        self.interface = toga.Font(self.font_family, self.font_size)
        self.impl = gtk_fonts.Font(self.interface)
        self.cache = gtk_fonts._FONT_CACHE
        self.assertEqual(self.cache[self.interface], self.impl.native)

    def test_font_family_defaults_to_system(self):
        self.interface = toga.Font(CURSIVE, self.font_size)
        self.native = self.interface._impl.native
        self.assertIn(CURSIVE, self.native.get_family())
        self.assertIn(SYSTEM, self.native.get_family())


if __name__ == '__main__':
    unittest.main()
