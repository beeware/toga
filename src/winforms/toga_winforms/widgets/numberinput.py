from toga_winforms.libs import WinForms, ClrDecimal

from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.native = WinForms.NumericUpDown()

    def get_value(self):
        raise NotImplementedError()

    def set_value(self, value):
        if value is not None and value is not "":
            self.native.Value = ClrDecimal.Parse(value)

    def rehint(self):
        self.interface.intrinsic.width = 120
        self.interface.intrinsic.height = 32
