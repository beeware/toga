from travertino.size import at_least

import toga

from ..libs import Gtk
from .base import Widget

# Implementation notes
# ====================
#
# We implement discrete mode as follows:
#   * Display ticks at each of the possible values.
#   * Intercept the change-value event, and round the value to the nearest tick.
#
# From GTK's point of view, these two features are independent, but we arrange for them
# to line up at the same values.


class Slider(Widget, toga.widgets.slider.SliderImpl):
    def create(self):
        self.adj = Gtk.Adjustment()
        self.native = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, self.adj)

        self.native.connect(
            "value-changed",
            lambda native: self.interface.on_change(None),
        )
        self.native.connect(
            "button-press-event",
            lambda native, event: self.interface.on_press(None),
        )
        self.native.connect(
            "button-release-event",
            lambda native, event: self.interface.on_release(None),
        )

        # Despite what the set_digits documentation says, set_round_digits has no effect
        # when set_draw_value is False, so we have to round the value manually. Disable
        # automatic rounding anyway, in case this changes in the future.
        self.native.set_round_digits(-1)
        self.native.set_draw_value(False)
        self.native.connect("change-value", self.gtk_change_value)

        # Dummy values used during initialization.
        self.tick_count = None

    def gtk_change_value(self, native, scroll_type, value):
        self.adj.set_value(self.interface._round_value(value))
        return True  # Disable default handler.

    def set_value(self, value):
        self.adj.set_value(value)

    def get_value(self):
        return self.native.get_value()

    def set_range(self, range):
        self.adj.set_lower(range[0])
        self.adj.set_upper(range[1])

    def get_range(self):
        return self.adj.get_lower(), self.adj.get_upper()

    def set_tick_count(self, tick_count):
        self.tick_count = tick_count
        self.native.clear_marks()
        if tick_count is not None:
            min, max = self.get_range()
            span = max - min
            for i in range(tick_count):
                value = min + (span * (i / (tick_count - 1)))
                self.native.add_mark(value, Gtk.PositionType.TOP)
                self.native.add_mark(value, Gtk.PositionType.BOTTOM)

    def get_tick_count(self):
        return self.tick_count

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        height = self.native.get_preferred_height()

        # Set intrinsic width to at least the minimum width
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        # Set intrinsic height to the natural height
        self.interface.intrinsic.height = height[1]
