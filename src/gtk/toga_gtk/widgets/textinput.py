from gi.repository import Gtk

from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = Gtk.Entry()
        self.native.interface = self.interface

        self.native.connect('show', lambda event: self.rehint())

    def set_readonly(self, value):
        self.native.editable = not value

    def set_placeholder(self, value):
        self.native.set_placeholder_text(value)

    def get_value(self):
        return self.native.get_text()

    def set_value(self, value):
        self.native.set_text(value)

    def rehint(self):
        # print("REHINT", self, self._impl.get_preferred_width(), self._impl.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
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
