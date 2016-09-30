from gi.repository import Gtk

from toga.interface import Button as ButtonInterface

from .base import WidgetMixin
from ..utils import wrapped_handler


class Button(ButtonInterface, WidgetMixin):
    def __init__(self, label, id=None, style=None, on_press=None):
        self._connections = []
        super().__init__(label, id=id, style=style, on_press=on_press)
        self._create()

    def create(self):
        self._impl = Gtk.Button()
        self._impl._interface = self

        self._impl.connect('show', lambda event: self.rehint())

    def _set_label(self, label):
        self._impl.set_label(self.label)
        self.rehint()

    def _set_on_press(self, handler):
        for conn_id in self._connections:
            # Disconnect all other on-click handlers, so that if you reassign
            # the on_press, it doesn't trigger the old ones too.
            self._impl.disconnect(conn_id)

        self._connections.append(
            self._impl.connect("clicked", wrapped_handler(self, handler)))

    def rehint(self):
        # print("REHINT", self, self._impl.get_preferred_width(), self._impl.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
        hints = {}
        width = self._impl.get_preferred_width()
        minimum_width = width[0]
        natural_width = width[1]

        height = self._impl.get_preferred_height()
        minimum_height = height[0]
        natural_height = height[1]

        if minimum_width > 0:
            hints['min_width'] = minimum_width
        if minimum_height > 0:
            hints['min_height'] = minimum_height
        if natural_height > 0:
            hints['height'] = natural_height

        if hints:
            self.style.hint(**hints)
