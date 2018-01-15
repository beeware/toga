from gi.repository import Gtk

from .base import Widget


class NumberInput(Widget):
    def create(self):
        adjustment = Gtk.Adjustment(0, self.interface.min_value,
                                    self.interface.max_value,
                                    self.interface.step, 10, 0)

        self.native = Gtk.SpinButton()
        self.native.set_adjustment(adjustment)
        self.native.set_numeric(True)
        self.native.interface = self.interface

        self.rehint()

    def set_readonly(self, value):
        self.native.editable = not value

    def set_step(self, step):
        raise NotImplementedError()

    def set_min_value(self, value):
        raise NotImplementedError()

    def set_max_value(self, value):
        raise NotImplementedError()

    def set_value(self, value):
        self.native.set_value(value)

    def set_alignment(self, value):
        raise NotImplementedError()

    def set_font(self, value):
        raise NotImplementedError()

    def rehint(self):
        self.interface.style.min_width = self.interface.MIN_WIDTH
        self.interface.style.height = 32

    def set_on_change(self, handler):
        # No special handling required.
        pass
