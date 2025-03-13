from travertino.size import at_least

from ..libs import GTK_VERSION, Gtk
from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = Gtk.Separator()

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            width = self.native.get_preferred_width()
            height = self.native.get_preferred_height()

            if self.get_direction() == self.interface.VERTICAL:
                self.interface.intrinsic.width = width[0]
                self.interface.intrinsic.height = at_least(height[1])
            else:
                self.interface.intrinsic.width = at_least(width[0])
                self.interface.intrinsic.height = height[1]
        else:  # pragma: no-cover-if-gtk3
            pass

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
