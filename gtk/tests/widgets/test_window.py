import unittest

try:
    import gi

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except ImportError:
    import sys

    # If we're on Linux, Gtk *should* be available. If it isn't, make
    # Gtk an object... but in such a way that every test will fail,
    # because the object isn't actually the Gtk interface.
    if sys.platform == "linux":
        Gtk = object()
    else:
        Gtk = None

import toga


def handle_events():
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)


@unittest.skipIf(
    Gtk is None, "Can't run GTK implementation tests on a non-Linux platform"
)
class TogaAppForWindowDemo(toga.App):
    pass


class TestGtkWindow(unittest.TestCase):
    def setUp(self):
        self.box1 = toga.Box()
        self.box2 = toga.Box()
        self.app = TogaAppForWindowDemo("Test", "org.beeware.toga-gtk-tests")
        self.app.main_window = toga.MainWindow("test window")
        self.window = self.app.main_window

    def test_set_content_visibility_effects(self):
        # Window is not showing, boxes cannot be drawn
        self.assertEqual(self.window._impl.get_visible(), False)
        self.assertEqual(self.box1._impl.native.is_drawable(), False)
        self.assertEqual(self.box2._impl.native.is_drawable(), False)

        self.window.content = self.box1
        self.assertEqual(self.window.content._impl.native.is_drawable(), False)

        self.window.content = self.box2
        self.assertEqual(self.window.content._impl.native.is_drawable(), False)

        self.window.show()
        self.assertEqual(self.window._impl.get_visible(), True)
        self.assertEqual(self.window.content._impl.native.is_drawable(), True)

        self.window.content = self.box1
        self.assertEqual(self.window._impl.get_visible(), True)
