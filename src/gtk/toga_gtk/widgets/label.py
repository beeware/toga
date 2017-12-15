from gi.repository import Gtk
from toga.constants import *
from toga_gtk.libs import gtk_alignment

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = Gtk.Label()
        self.native.set_line_wrap(False)

        self.native.interface = self.interface

        self.native.connect('show', lambda event: self.rehint())

    def set_alignment(self, value):
        self.native.set_alignment(*gtk_alignment(value))

    def set_text(self, value):
        # FIXME after setting the label the label jumps to the top left
        # corner and only jumps back at its place after resizing the window.
        self.native.set_text(value)

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

        if hints:
            self.interface.style.hint(**hints)