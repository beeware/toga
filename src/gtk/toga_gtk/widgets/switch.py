from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class Switch(Widget):
    def create(self):
        self.native = Gtk.Box()
        self.native.interface = self.interface

        self.label = Gtk.Label(xalign=0)
        self.label.set_line_wrap(True)

        self.switch = Gtk.Switch()
        self.switch.connect("notify::active", self.gtk_on_change)

        self.native.pack_start(self.label, True, True, 0)
        self.native.pack_start(self.switch, False, False, 0)
        self.native.connect('show', lambda event: self.rehint())

    def gtk_on_change(self, widget, state):
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    def set_on_change(self, handler):
        pass

    def set_text(self, text):
        self.label.set_text(self.interface.text)

    def get_value(self):
        return self.switch.get_active()

    def set_value(self, value):
        self.switch.set_active(value)

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        # Set intrinsic width to at least the minimum width
        self.interface.intrinsic.width = at_least(width[0])
        # Set intrinsic height to the natural height
        self.interface.intrinsic.height = height[1]
