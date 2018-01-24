from toga_winforms.libs import WinForms, ClrDecimal

from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.native = WinForms.NumericUpDown()

    def set_readonly(self, value):
        self.interface.factory.not_implemented('NumberInput.set_readonly()')

    def set_step(self, step):
        self.interface.factory.not_implemented('NumberInput.set_step()')

    def set_min_value(self, value):
        self.interface.factory.not_implemented('NumberInput.set_min_value()')

    def set_max_value(self, value):
        self.interface.factory.not_implemented('NumberInput.set_max_value()')

    def set_value(self, value):
        if value is not None and value is not "":
            self.native.Value = ClrDecimal.Parse(value)

    def set_alignment(self, value):
        self.interface.factory.not_implemented('NumberInput.set_alignment()')

    def set_font(self, value):
        self.interface.factory.not_implemented('NumberInput.set_font()')

    def rehint(self):
        self.interface.intrinsic.width = 120
        self.interface.intrinsic.height = 32

    def set_on_change(self, handler):
        self.interface.factory.not_implemented('NumberInput.set_on_change()')
