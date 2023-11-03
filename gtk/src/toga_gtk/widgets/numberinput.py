import sys
from decimal import InvalidOperation

from travertino.size import at_least

from toga.widgets.numberinput import _clean_decimal

from ..libs import Gtk, gtk_alignment
from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.adjustment = Gtk.Adjustment()

        self.native = Gtk.SpinButton()
        self.native.set_adjustment(self.adjustment)
        self.native.set_numeric(True)

        self.native.connect("changed", self.gtk_on_change)

    def gtk_on_change(self, widget):
        self.interface.on_change()

    def get_readonly(self):
        return not self.native.get_property("editable")

    def set_readonly(self, value):
        self.native.set_property("editable", not value)

    def set_step(self, step):
        self.adjustment.set_step_increment(float(self.interface.step))
        self.native.set_adjustment(self.adjustment)
        self.native.set_digits(abs(self.interface.step.as_tuple().exponent))

    def set_min_value(self, value):
        if value is None:
            self.adjustment.set_lower(-sys.float_info.max)
        else:
            self.adjustment.set_lower(float(value))
        self.native.set_adjustment(self.adjustment)

    def set_max_value(self, value):
        if value is None:
            self.adjustment.set_upper(sys.float_info.max)
        else:
            self.adjustment.set_upper(float(value))
        self.native.set_adjustment(self.adjustment)

    def get_value(self):
        try:
            return _clean_decimal(self.native.get_text(), self.interface.step)
        except InvalidOperation:
            return None

    def set_value(self, value):
        if value is None:
            self.native.set_value(0)
        else:
            self.native.set_value(value)

    def set_alignment(self, value):
        xalign, justify = gtk_alignment(value)
        self.native.set_alignment(xalign)

    def rehint(self):
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, width[1])
        )
        self.interface.intrinsic.height = height[1]
