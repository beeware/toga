from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = Gtk.Separator

    def rehint(self):
        min_size, size = self.native.get_preferred_size()

        if self.get_direction() == self.interface.VERTICAL:
            self.interface.intrinsic.width = min_size.width
            self.interface.intrinsic.height = at_least(size.height)
        else:
            self.interface.intrinsic.width = at_least(min_size.width)
            self.interface.intrinsic.height = size.height

    def get_direction(self):
        return (
            self.interface.VERTICAL
            if self.native.get_orientation() == Gtk.Orientation.VERTICAL
            else self.interface.HORIZONTAL
        )

    def set_direction(self, value):
        if value == self.interface.VERTICAL:
            self.native.set_orientation(Gtk.Orientation.VERTICAL)
        else:
            self.native.set_orientation(Gtk.Orientation.HORIZONTAL)
