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

from toga_gtk.widgets.imageview import ImageView


@unittest.skipIf(Gtk is None, "Can't run GTK implementation tests on a non-Linux platform")
class TestGtkImageView(unittest.TestCase):

    def test_resize_max(self):

        # Scale up height bound
        self.assertEqual((500, 500), ImageView._resize_max(250, 250, 500, 1000))

        # Scale up width bound
        self.assertEqual((500, 500), ImageView._resize_max(250, 250, 1000, 500))

        # Scale down height bound
        self.assertEqual((250, 166), ImageView._resize_max(750, 500, 250, 250))

        # Scale down width bound
        self.assertEqual((166, 250), ImageView._resize_max(500, 750, 250, 250))

        # Invalid max(target) size
        self.assertEqual((1, 1), ImageView._resize_max(500, 750, 250, -1))
        self.assertEqual((1, 1), ImageView._resize_max(500, 750, 0, 250))
