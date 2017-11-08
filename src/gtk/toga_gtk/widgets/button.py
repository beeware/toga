from gi.repository import Gtk

from .base import Widget


class Button(Widget):
    def create(self):
        self._on_press_handler = None

        self.native = Gtk.Button()
        self.native.interface = self.interface
        self.native.connect("clicked", self._on_press)

        self.native.connect('show', lambda event: self.rehint())

    def set_label(self, label):
        self.native.set_label(label)
        self.rehint()

    def set_enabled(self, value):
        # self._impl.set_sensitive(value)
        pass

    def set_background_color(self, value):
        pass

    def _on_press(self, widget):
        if self._on_press_handler:
            self._on_press_handler(widget)

    def set_on_press(self, handler):
        self._on_press_handler = handler

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
