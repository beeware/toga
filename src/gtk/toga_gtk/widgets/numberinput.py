from gi.repository import Gtk
from .base import Widget


class NumberInput(Widget):
    def create(self):
        adjustment = Gtk.Adjustment(0, self.interface._min_value,
                                    self.interface._max_value,
                                    self.interface._step, 10, 0)

        self.native = Gtk.SpinButton()
        self.native.set_adjustment(adjustment)
        self.native.set_numeric(True)
        self.native.interface = self.interface

        self.rehint()

    def get_value(self):
        return self.native.get_value()

    def set_value(self, value):
        self.native.set_value(value)

    def rehint(self):
        self.interface.style.min_width = 120
        self.interface.style.height = 32
