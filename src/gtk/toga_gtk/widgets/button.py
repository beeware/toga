from gi.repository import Gtk

from .base import Widget
from ..utils import wrapped_handler


class Button(Widget):
    def create(self):
        self._connections = []
        self.native = Gtk.Button()
        self.native.interface = self.interface

        self.native.connect('show', lambda event: self.rehint())

    def set_label(self, label):
        self.native.set_label(label)
        self.rehint()

    def set_enabled(self, value):
        # self._impl.set_sensitive(value)
        pass

    def set_background_color(self, value):
        pass

    def set_on_press(self, handler):
        for conn_id in self._connections:
            # Disconnect all other on-click handlers, so that if you reassign
            # the on_press, it doesn't trigger the old ones too.
            self.native.disconnect(conn_id)

        self._connections.append(
            self.native.connect("clicked", wrapped_handler(self.interface, handler)))

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
        hints = {}
        width = self.native.get_preferred_width()
        minimum_width = width[0]
        natural_width = width[1]

        height = self.native.get_preferred_height()
        minimum_height = height[0]
        natural_height = height[1]

        if minimum_width > 0:
            hints['min_width'] = minimum_width
        if minimum_height > 0:
            hints['min_height'] = minimum_height
        if natural_height > 0:
            hints['height'] = natural_height

        if hints:
            self.interface.style.hint(**hints)
