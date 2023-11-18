import sys
from decimal import ROUND_UP, Decimal, InvalidOperation

import System.Windows.Forms as WinForms
from System import Convert, String

from toga.widgets.numberinput import _clean_decimal
from toga_winforms.libs.fonts import HorizontalTextAlignment

from ..libs.wrapper import WeakrefCallable
from .base import Widget


def native_decimal(value):
    if isinstance(value, Decimal):
        # The explicit type is needed to prevent single-character strings from calling
        # the Char overload, which always throws an exception.
        return Convert.ToDecimal.__overloads__[String](str(value))
    else:
        assert isinstance(value, int)
        return Convert.ToDecimal(value)


class NumberInput(Widget):
    _background_supports_alpha = False

    def create(self):
        self.native = WinForms.NumericUpDown()
        self.native.TextChanged += WeakrefCallable(self.winforms_text_changed)

    def winforms_text_changed(self, sender, event):
        self.interface.on_change()

    def get_readonly(self):
        return self.native.ReadOnly

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def set_step(self, step):
        self.native.Increment = native_decimal(step)
        self.native.DecimalPlaces = abs(step.as_tuple().exponent)

    def set_min_value(self, value):
        self.native.Minimum = native_decimal(
            (-sys.maxsize - 1) if value is None else value,
        )

    def set_max_value(self, value):
        self.native.Maximum = native_decimal(
            sys.maxsize if value is None else value,
        )

    def get_value(self):
        try:
            return _clean_decimal(self.native.Text, self.interface.step)
        except InvalidOperation:
            return None

    def set_value(self, value):
        if value is None:
            self.native.Text = ""
        else:
            self.native.Value = native_decimal(value)

    def set_alignment(self, value):
        self.native.TextAlign = HorizontalTextAlignment(value)

    def rehint(self):
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )
