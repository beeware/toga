from toga_winforms.libs import LEFT, RIGHT, CENTER
from toga_winforms.libs import WinForms, Convert

from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.native = WinForms.NumericUpDown()

    def set_readonly(self, value):
        self.native.ReadOnly = self.interface.readonly

    def set_step(self, step):
        self.native.Increment = Convert.ToDecimal(self.interface.step)

    def set_min_value(self, value):
        if self.interface.min_value is not None:
            self.native.Minimum = Convert.ToDecimal(self.interface.min_value)

    def set_max_value(self, value):
        if self.interface.max_value is not None:
            self.native.Maximum = Convert.ToDecimal(self.interface.max_value)

    def set_value(self, value):
        if value is not None and value is not "":
            self.native.Value = Convert.ToDecimal(self.interface.value)

    def set_alignment(self, value):
        if value is not None:
            if value == CENTER:
                self.native.TextAlign = WinForms.HorizontalAlignment.Center
            elif value == LEFT:
                self.native.TextAlign = WinForms.HorizontalAlignment.Left
            elif value == RIGHT:
                self.native.TextAlign = WinForms.HorizontalAlignment.Right
            else:
                self.interface.factory.not_implemented(
                    'NumberInput.set_alignment() with anything else but center, left and right')

    def set_font(self, value):
        self.interface.factory.not_implemented('NumberInput.set_font()')

    def rehint(self):
        self.interface.intrinsic.width = 120
        self.interface.intrinsic.height = 32

    def set_on_change(self, handler):
        self.interface.factory.not_implemented('NumberInput.set_on_change()')
