import sys

from travertino.size import at_least

from toga_winforms.libs import Convert, HorizontalTextAlignment, WinForms

from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.native = WinForms.NumericUpDown()
        self.native.Value = Convert.ToDecimal(0.0)
        self.native.ValueChanged += self.winforms_value_changed

    def winforms_value_changed(self, sender, event):
        if self.container:
            self.interface.value = Convert.ToString(sender.Value)
            if self.interface.on_change:
                self.interface.on_change(self.interface)

    def set_readonly(self, value):
        self.native.ReadOnly = self.interface.readonly

    def set_step(self, step):
        self.native.Increment = Convert.ToDecimal(float(self.interface.step))
        self.native.DecimalPlaces = abs(self.interface.step.as_tuple().exponent)

    def set_min_value(self, value):
        if self.interface.min_value is None:
            self.native.Minimum = Convert.ToDecimal(-sys.maxsize - 1)
        else:
            self.native.Minimum = Convert.ToDecimal(float(self.interface.min_value))

    def set_max_value(self, value):
        if self.interface.max_value is None:
            self.native.Maximum = Convert.ToDecimal(sys.maxsize)
        else:
            self.native.Maximum = Convert.ToDecimal(float(self.interface.max_value))

    def set_value(self, value):
        if value is None or value == '':
            self.native.Value = Convert.ToDecimal(0.0)
        else:
            self.native.Value = Convert.ToDecimal(float(self.interface.value))

    def set_alignment(self, value):
        self.native.TextAlign = HorizontalTextAlignment(value)

    def set_font(self, font):
        if font:
            self.native.Font = font.bind(self.interface.factory).native

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_on_change(self, handler):
        pass
