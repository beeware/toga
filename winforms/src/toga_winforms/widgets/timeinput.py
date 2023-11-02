import datetime
from decimal import ROUND_UP

import System.Windows.Forms as WinForms
from System import DateTime as WinDateTime

from ..libs.wrapper import WeakrefCallable
from .base import Widget


def py_time(native_time):
    return datetime.time(native_time.Hour, native_time.Minute, native_time.Second)


def native_time(py_time):
    # We don't need the date component, so we can use any date as long as we're
    # consistent.
    return WinDateTime(1970, 1, 1, py_time.hour, py_time.minute, py_time.second)


class TimeInput(Widget):
    _background_supports_alpha = False

    def create(self):
        self.native = WinForms.DateTimePicker()
        self.native.ValueChanged += WeakrefCallable(self.winforms_value_changed)
        self.native.Format = WinForms.DateTimePickerFormat.Time
        self.native.ShowUpDown = True

    def get_value(self):
        return py_time(self.native.Value)

    def set_value(self, value):
        self.native.Value = native_time(value)

    def get_min_time(self):
        return py_time(self.native.MinDate)

    def set_min_time(self, value):
        self.native.MinDate = native_time(value)

    def get_max_time(self):
        return py_time(self.native.MaxDate)

    def set_max_time(self, value):
        self.native.MaxDate = native_time(value)

    def rehint(self):
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )

    def winforms_value_changed(self, sender, event):
        self.interface.on_change()
