import datetime
from decimal import ROUND_UP

import System.Windows.Forms as WinForms
from System import DateTime as WinDateTime

from ..libs.wrapper import WeakrefCallable
from .base import Widget


def py_date(native_date):
    return datetime.date(native_date.Year, native_date.Month, native_date.Day)


def native_date(py_date):
    return WinDateTime(py_date.year, py_date.month, py_date.day)


class DateInput(Widget):
    _background_supports_alpha = False

    def create(self):
        self.native = WinForms.DateTimePicker()
        self.native.ValueChanged += WeakrefCallable(self.winforms_value_changed)

    def get_value(self):
        return py_date(self.native.Value)

    def set_value(self, value):
        self.native.Value = native_date(value)

    def get_min_date(self):
        return py_date(self.native.MinDate)

    def set_min_date(self, value):
        self.native.MinDate = native_date(value)

    def get_max_date(self):
        return py_date(self.native.MaxDate)

    def set_max_date(self, value):
        self.native.MaxDate = native_date(value)

    def rehint(self):
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )

    def winforms_value_changed(self, sender, event):
        self.interface.on_change()
