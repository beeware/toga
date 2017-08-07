from __future__ import print_function, absolute_import, division

from gi.repository import Gtk
from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        self.native = Gtk.TextView()
        self.native.interface = self.interface
        self.buffer = Gtk.TextBuffer()
        self.native.set_buffer(self.buffer)

    def set_value(self, value):
        self.buffer.set_text(value)

    def get_value(self):
        return self.buffer.get_text(None, None, True)

    def set_readonly(self, value):
        self.native.editable = value

    # @property
    # def _width_hint(self):
    #     print("WIDGET WIDTH", self, self.native.get_preferred_width())
    #     return self.native.get_preferred_width()
    #
    # @property
    # def _height_hint(self):
    #     print("WIDGET HEIGHT", self, self.native.get_preferred_height())
    #     return self.native.get_preferred_height()
