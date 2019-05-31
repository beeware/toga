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


def handle_events():
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)


@unittest.skipIf(Gtk is None, "Can't run GTK implementation tests on a non-Linux platform")
class TestGtkSwitch(unittest.TestCase):
    def setUp(self):
        self.switch = toga.Switch(label='A switch')

        # make a shortcut for easy use
        self.gtk_switch = self.switch._impl

        self.window = Gtk.Window()
        self.window.add(self.switch._impl.native)

    def test_set_label(self):
        self.assertEqual(self.switch.label, 'A switch')
        self.switch.label = 'New'
        self.assertEqual(self.switch.label, 'New')
        self.assertEqual(self.switch._label, 'New')

    def test_set_is_on(self):
        self.assertEqual(self.switch.is_on, False)
        self.switch.is_on = True
        self.assertEqual(self.switch.is_on, True)
