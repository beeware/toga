from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class Button(Widget):
    def create(self):
        self.native = Gtk.Button()
        self.native.interface = self.interface

        self.native.connect('show', lambda event: self.rehint())
        self.native.connect('clicked', self.gtk_on_press)

    def set_label(self, label):
        self.native.set_label(self.interface.label)
        self.rehint()

    def set_enabled(self, value):
        self.native.set_sensitive(value)

    def set_background_color(self, value):
        self.interface.factory.not_implemented('Button.set_background_color()')

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[1]

    def gtk_on_press(self, event):
        self.interface.raise_event('on_press')
