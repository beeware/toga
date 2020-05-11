from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class Slider(Widget):
    def create(self):
        self.adj = Gtk.Adjustment()

        self.native = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, self.adj)
        self.native.interface = self.interface
        self.native.connect("value-changed", self.gtk_on_slide)

        self.rehint()

    def gtk_on_slide(self, widget):
        if self.interface.on_slide:
            self.interface.on_slide(widget)

    def set_on_slide(self, handler):
        # No special handling required
        pass

    def set_value(self, value):
        self.adj.set_value(value)

    def get_value(self):
        return self.native.get_value()

    def set_range(self, range):
        self.adj.set_lower(self.interface.range[0])
        self.adj.set_upper(self.interface.range[1])

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        # Set intrinsic width to at least the minimum width
        self.interface.intrinsic.width = at_least(width[0])
        # Set intrinsic height to the natural height
        self.interface.intrinsic.height = height[1]

