from gi.repository import Gtk

from .base import Widget


class Slider(Widget):
    def create(self):
        self.adj = Gtk.Adjustment()

        self.native = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, self.adj)
        self.native.interface = self.interface
        self.native.connect("value-changed", self._on_slide)

        self.rehint()

    def _on_slide(self, widget):
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
        self.adj.set_lower(range[0])
        self.adj.set_upper(range[1])

    def rehint(self):
        hints = {}
        width = self.native.get_preferred_width()
        minimum_width = 160
        natural_width = width[1]

        height = self.native.get_preferred_height()
        minimum_height = height[0]
        natural_height = height[1]

        if minimum_width > 0:
            hints['min_width'] = minimum_width
        if minimum_height > 0:
            hints['min_height'] = minimum_height
        if natural_width > 0:
            hints['width'] = natural_width
        if natural_height > 0:
            hints['height'] = natural_height

        if hints:
            self.interface.style.hint(**hints)
