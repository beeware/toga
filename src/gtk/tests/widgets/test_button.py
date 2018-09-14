import unittest
import gi
import toga
from toga.constants import RED

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk  # noqa: E402


def handle_events():
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)


class TestGtkButton(unittest.TestCase):
    def setUp(self):
        self.btn = toga.Button('test_btn')
        self._gtk_btn = self.btn._impl
        self._native = self._gtk_btn.native

    def test_label(self):
        self.assertEqual(self._native.get_label(), self.btn.label)

    def test_is_enabled(self):
        self.btn.enabled = True
        self.assertTrue(self._native.is_sensitive())

    def test_is_disabled(self):
        self.btn.enabled = False
        self.assertFalse(self._native.is_sensitive())

    def test_set_background_color(self):
        self.btn.style.background_color = RED
        # `gtk_background_color` is deprecated,
        # and cannot be used to fetch gradients as background but simple colors work fine
        self.assertEqual(
            self._native.get_style_context().get_background_color(
                self._native.get_state_flags()).to_color(),
            Gdk.RGBA(1.0, 0.0, 0.0, 0.0).to_color())

    def test_rehint(self):
        pass


if __name__ == '__main__':
    unittest.main()
