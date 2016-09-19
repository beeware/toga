from gi.repository import Gtk

from toga.interface import Button as ButtonInterface

from .base import WidgetMixin
from ..utils import wrapped_handler


class Button(ButtonInterface, WidgetMixin):
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(label, id=id, style=style, on_press=on_press)
        self._create()

        # Buttons have a fixed drawn height. If their space allocation is
        # greater than what is provided, center the button vertically.
        self._fixed_height = True

    def create(self):
        self._impl = Gtk.Button()
        self._impl._interface = self

        self._impl.connect('show', lambda event: self.rehint())

    def _set_label(self, label):
        self._impl.set_label(self.label)
        self.rehint()

    def _set_on_press(self, handler):
        self._impl.connect("clicked", wrapped_handler(self, handler))
