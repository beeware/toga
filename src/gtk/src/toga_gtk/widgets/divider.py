from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = Gtk.Separator()
        self.native.interface = self.interface

    def rehint(self):
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        if self.interface.direction == self.interface.VERTICAL:
            self.interface.intrinsic.width = width[0]
            self.interface.intrinsic.height = at_least(height[1])
        else:
            self.interface.intrinsic.width = at_least(width[0])
            self.interface.intrinsic.height = height[1]

    def set_direction(self, value):
        if value == self.interface.VERTICAL:
            self.native.set_orientation(Gtk.Orientation.VERTICAL)
        else:
            self.native.set_orientation(Gtk.Orientation.HORIZONTAL)
