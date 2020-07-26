import unittest

import toga
from toga_gtk import factory as gtk_factory
from toga.constants import BOLD, CURSIVE, ITALIC, OBLIQUE, SMALL_CAPS, SYSTEM
from toga_gtk import fonts as gtk_fonts

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
        self.font_family = SYSTEM
        self.font_size = 12

    def test_font_default_has_all_attr_set(self):
        font = toga.Font(self.font_family, self.font_size)
        native = font.bind(gtk_factory).native
        self.assertEqual(native.get_family(), SYSTEM)
        self.assertEqual(native.get_size() / Pango.SCALE, self.font_size)
        self.assertEqual(native.get_style(), Pango.Style.NORMAL)
        self.assertEqual(native.get_variant(), Pango.Variant.NORMAL)
        self.assertEqual(native.get_weight(), Pango.Weight.NORMAL)

    def test_font_size(self):
        self.font_size = 22
        font = toga.Font(self.font_family, self.font_size)
        native = font.bind(gtk_factory).native
        self.assertEqual(native.get_size() / Pango.SCALE, self.font_size)

    def test_font_style_italic(self):
        font = toga.Font(
            self.font_family, self.font_size, style=ITALIC)
        native = font.bind(gtk_factory).native
        self.assertEqual(native.get_style(), Pango.Style.ITALIC)

    def test_font_style_oblique(self):
        font = toga.Font(
            self.font_family, self.font_size, style=OBLIQUE)
        native = font.bind(gtk_factory).native
        self.assertEqual(native.get_style(), Pango.Style.OBLIQUE)

    def test_font_variant_small_caps(self):
        font = toga.Font(
            self.font_family, self.font_size, variant=SMALL_CAPS)
        native = font.bind(gtk_factory).native
        self.assertEqual(native.get_variant(), Pango.Variant.SMALL_CAPS)

    def test_font_weight_bold(self):
        font = toga.Font(
            self.font_family, self.font_size, weight=BOLD)
        native = font.bind(gtk_factory).native
        self.assertEqual(native.get_weight(), Pango.Weight.BOLD)

    def test_font_cache(self):
        font = toga.Font(self.font_family, self.font_size)
        self.impl = gtk_fonts.Font(font)
        self.cache = gtk_fonts._FONT_CACHE
        self.assertEqual(self.cache[font], self.impl.native)

    def test_font_family_defaults_to_system(self):
        font = toga.Font(CURSIVE, self.font_size)
        native = font.bind(gtk_factory).native
        self.assertIn(CURSIVE, native.get_family())
        self.assertIn(SYSTEM, native.get_family())


if __name__ == '__main__':
    unittest.main()
