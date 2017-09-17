from ..libs import WinForms, ClrDecimal
from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.native = WinForms.NumericUpDown()

    def set_value(self, value):
        if value is not None and value is not "":
            self.native.Value = ClrDecimal.Parse(value)

    def rehint(self):
        self.style.min_width = 120
        self.style.height = 32
