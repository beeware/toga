from gi.repository import Gtk
import sys
from travertino.constants import LEFT, RIGHT

from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.interface.adjustment = Gtk.Adjustment(0, -sys.maxsize, sys.maxsize,
                                                    1, 10, 0)
        self.native = Gtk.SpinButton()
        self.native.set_numeric(True)
        self.native.interface = self.interface

        self.native.set_adjustment(self.interface.adjustment)
        self.rehint()

    def set_readonly(self, value):
        self.native.set_property('editable', not value)

    def set_step(self, step):
        if step:
            self.native.set_increments(step,step)

    def set_min_value(self, value):
        if value:
            self.interface.adjustment.set_lower(self.interface.min_value)

    def set_max_value(self, value):
        if value:
            self.interface.adjustment.set_upper(self.interface.max_value)

    def set_value(self, value):
        self.native.set_value(value)

    def set_alignment(self, value):
        if value == LEFT:
            self.native.set_alignment(0)
        elif value == RIGHT:
            self.native.set_alignment(1)
        else:
            try:
                float(value) >=0.0 and float(value) <=1.0
                self.native.set_alignment(float(value))
            except TypeError:
                raise TypeError("Alighment can either be LEFT/RIGHT or a float from 0 1o 1")

    def set_font(self, value):
        if value:
            self.native.modify_font(value._impl.native)

    def rehint(self):
        self.interface.style.min_width = self.interface.MIN_WIDTH
        self.interface.style.height = 32

    def set_on_change(self, handler):
        # No special handling required.
        pass
