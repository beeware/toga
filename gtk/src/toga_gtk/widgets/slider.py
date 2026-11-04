from travertino.size import at_least

from toga.handlers import WeakrefCallable
from toga.widgets.slider import SliderImpl

from ..libs import GTK_VERSION, Gtk
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


class Slider(Widget, SliderImpl):
    def create(self):
        self.adj = Gtk.Adjustment()
        self.native = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, self.adj)

        self.native.connect("value-changed", WeakrefCallable(self.gtk_on_change))
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.connect(
                "button-press-event",
                WeakrefCallable(self.gtk_on_press),
            )
            self.native.connect(
                "button-release-event",
                WeakrefCallable(self.gtk_on_release),
            )
        else:  # pragma: no-cover-if-gtk3
            self.click_controller = Gtk.GestureClick()
            self.click_controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            self.click_controller.connect("pressed", WeakrefCallable(self.gtk_on_press))
            self.click_controller.connect(
                "released", WeakrefCallable(self.gtk_on_release)
            )
            self.native.add_controller(self.click_controller)

        # Despite what the set_digits documentation says, set_round_digits has no
        # effect when set_draw_value is False, so we have to round the value
        # manually. Disable automatic rounding anyway, in case this changes in the
        # future.
        self.native.set_round_digits(-1)
        self.native.set_draw_value(False)
        self.native.connect("change-value", WeakrefCallable(self.gtk_change_value))

        # Dummy values used during initialization.
        self.tick_count = None

    def gtk_on_change(self, *_args):
        self.interface.on_change()

    def gtk_on_press(self, *_args):
        self.interface.on_press()

    def gtk_on_release(self, *_args):
        self.interface.on_release()

    def gtk_change_value(self, native, scroll_type, value):
        self.adj.set_value(self.interface._round_value(value))
        return True  # Disable default handler.

    def set_value(self, value):
        self.adj.set_value(value)

    def get_value(self):
        return self.native.get_value()

    def get_min(self):
        return self.adj.get_lower()

    def set_min(self, value):
        self.adj.set_lower(value)

    def get_max(self):
        return self.adj.get_upper()

    def set_max(self, value):
        self.adj.set_upper(value)

    def set_tick_count(self, tick_count):
        self.tick_count = tick_count
        self.native.clear_marks()
        if tick_count is not None:
            min = self.get_min()
            max = self.get_max()
            span = max - min
            for i in range(tick_count):
                value = min + (span * (i / (tick_count - 1)))
                self.native.add_mark(value, Gtk.PositionType.TOP)
                self.native.add_mark(value, Gtk.PositionType.BOTTOM)

    def get_tick_count(self):
        return self.tick_count

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # print(
            #     "REHINT",
            #     self,
            #     self.native.get_preferred_width(),
            #     self.native.get_preferred_height(),
            # )
            height = self.native.get_preferred_height()

            # Set intrinsic width to at least the minimum width
            self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
            # Set intrinsic height to the natural height
            self.interface.intrinsic.height = height[1]
        else:  # pragma: no-cover-if-gtk3
            _, size = self.native.get_preferred_size()

            self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
            self.interface.intrinsic.height = size.height
