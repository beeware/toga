from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class Slider(Widget):
    def create(self):
        self.adj = Gtk.Adjustment()

        self.native = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, self.adj)
        self.native.interface = self.interface
        self.native.connect("value-changed", self.gtk_on_change)

        self.rehint()

    def gtk_on_change(self, widget):
        if self.interface.on_change:
            self.interface.on_change(widget)

    def set_on_change(self, handler):
        # No special handling required
        pass

    def set_on_press(self, handler):
        self.interface.factory.not_implemented("Slider.set_on_press()")

    def set_on_release(self, handler):
        self.interface.factory.not_implemented("Slider.set_on_release()")

    def set_value(self, value):
        self.adj.set_value(value)

    def get_value(self):
        return self.native.get_value()

    def set_range(self, range):
        self.adj.set_lower(self.interface.range[0])
        self.adj.set_upper(self.interface.range[1])

    def set_tick_count(self, tick_count):
        self.interface.factory.not_implemented('Slider.tick_count()')

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        height = self.native.get_preferred_height()

        # Set intrinsic width to at least the minimum width
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        # Set intrinsic height to the natural height
        self.interface.intrinsic.height = height[1]
