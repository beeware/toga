import sys
from decimal import Decimal

from travertino.size import at_least

from gi.repository import Gtk

from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.adjustment = Gtk.Adjustment()

        self.native = Gtk.SpinButton()
        self.native.interface = self.interface
        self.native.set_adjustment(self.adjustment)
        self.native.set_numeric(True)

        self.native.connect("value-changed", self._on_change)

        self.rehint()

    def _on_change(self, widget):
        self.interface._value = Decimal(self.native.get_value()).quantize(self.interface.step)
        if self.interface.on_change:
            self.interface.on_change(widget)

    def set_readonly(self, value):
        self.native.editable = not value

    def set_step(self, step):
        self.adjustment.set_step_increment(float(self.interface.step))
        self.native.set_adjustment(self.adjustment)
        self.native.set_digits(abs(self.interface.step.as_tuple().exponent))

    def set_min_value(self, value):
        if self.interface.min_value is None:
            self.adjustment.set_lower(-sys.maxsize - 1)
        else:
            self.adjustment.set_lower(float(self.interface.min_value))
        self.native.set_adjustment(self.adjustment)

    def set_max_value(self, value):
        if self.interface.max_value is None:
            self.adjustment.set_upper(sys.maxsize)
        else:
            self.adjustment.set_upper(float(self.interface.max_value))
        self.native.set_adjustment(self.adjustment)

    def set_value(self, value):
        if value is None:
            self.native.set_value(Decimal(0.0))
        else:
            self.native.set_value(self.interface.value)

    def set_alignment(self, value):
        self.interface.factory.not_implemented('NumberInput.set_alignment()')

    def set_font(self, value):
        self.interface.factory.not_implemented('NumberInput.set_font()')

    def rehint(self):
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()
        if width and height:
            self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
            self.interface.intrinsic.height = height[1]

    def set_on_change(self, handler):
        # No special handling required.
        pass
