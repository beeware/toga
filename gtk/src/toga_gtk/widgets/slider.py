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

        self.native.connect("value-changed", self.gtk_on_change)

        click_gesture = Gtk.GestureClick.new()
        click_gesture.set_button(1)  # Montoring left mouse button
        click_gesture.set_propagation_phase(Gtk.PropagationPhase.BUBBLE)
        click_gesture.connect("end", self.gtk_on_end)
        click_gesture.connect("pressed", self.gtk_on_press)
        click_gesture.connect("unpaired-release", self.gtk_on_unpair_release)
        self.native.add_controller(click_gesture)

        # Despite what the set_digits documentation says, set_round_digits has no effect
        # when set_draw_value is False, so we have to round the value manually. Disable
        # automatic rounding anyway, in case this changes in the future.
        self.native.set_round_digits(-1)
        self.native.set_draw_value(False)
        self.native.connect("change-value", self.gtk_change_value)

        # Dummy values used during initialization.
        self.tick_count = None

    def gtk_on_change(self, widget):
        if self.interface.on_change:
            self.interface.on_change(widget)

    def gtk_on_press(self, widget, n_press, x, y):
        if self.interface.on_press:
            self.interface.on_press(widget)

    def gtk_on_end(self, widget, sequence):
        if self.interface.on_release:
            self.interface.on_release(widget)

    def gtk_on_unpair_release(self, widget, x, y, button, sequence):
        if self.interface.on_release:
            self.interface.on_release(widget)

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
        # print(
        #     "REHINT",
        #     self,
        #     self.native.get_preferred_size()[0].width,
        #     self.native.get_preferred_size()[0].height,
        # )
        min_size, size = self.native.get_preferred_size()

        # Set intrinsic width to at least the minimum width
        self.interface.intrinsic.width = at_least(
            max(min_size.width, self.interface._MIN_WIDTH)
        )
        # Set intrinsic height to the natural height
        self.interface.intrinsic.height = size.height
