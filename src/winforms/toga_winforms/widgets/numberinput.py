from toga_winforms.libs import WinForms, ClrDecimal

from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.native = WinForms.NumericUpDown()

    def set_readonly(self, value):
        raise NotImplementedError()

    def set_step(self, step):
        raise NotImplementedError()

    def set_min_value(self, value):
        raise NotImplementedError()

    def set_max_value(self, value):
        raise NotImplementedError()

    def set_value(self, value):
        if value is not None and value is not "":
            self.native.Value = ClrDecimal.Parse(value)

    def set_alignment(self, value):
        raise NotImplementedError()

    def set_font(self, value):
        raise NotImplementedError()

    def rehint(self):
        self.interface.intrinsic.width = 120
        self.interface.intrinsic.height = 32

    def set_on_change(self, handler):
        raise NotImplementedError()
