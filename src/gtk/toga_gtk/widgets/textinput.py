from gi.repository import Gtk
from travertino.size import at_least

from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = Gtk.Entry()
        self.native.interface = self.interface

        self.native.connect('show', lambda event: self.rehint())

    def set_readonly(self, value):
        self.native.set_property('editable', not value)

    def set_placeholder(self, value):
        self.native.set_placeholder_text(value)

    def set_alignment(self, value):
        self.interface.factory.not_implemented('TextInput.set_alignment()')

    def set_font(self, value):
        self.interface.factory.not_implemented('TextInput.set_font()')

    def get_value(self):
        return self.native.get_text()

    def set_value(self, value):
        self.native.set_text(value)

    def rehint(self):
        # print("REHINT", self, self._impl.get_preferred_width(), self._impl.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = height[1]

    def set_on_change(self, handler):
        # No special handling required
        pass
