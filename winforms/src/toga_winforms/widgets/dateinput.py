import datetime

from travertino.size import at_least

from toga_winforms.libs import WinDateTime, WinForms

from .base import Widget

NO_MIN = WinForms.DateTimePicker.MinDateTime  # Year 1753
NO_MAX = WinForms.DateTimePicker.MaxDateTime  # Year 9998


def py_date(native_date):
    return datetime.date(native_date.Year, native_date.Month, native_date.Day)


def native_date(py_date):
    return WinDateTime(py_date.year, py_date.month, py_date.day)


class DateInput(Widget):
    _background_supports_alpha = False

    def create(self):
        self.native = WinForms.DateTimePicker()
        self.native.ValueChanged += self.winforms_value_changed

    def get_value(self):
        return py_date(self.native.Value)

    def set_value(self, value):
        self.native.Value = native_date(value)

    def get_min_date(self):
        if self.native.MinDate == NO_MIN:
            return None
        return py_date(self.native.MinDate)

    def set_min_date(self, value):
        self.native.MinDate = NO_MIN if value is None else native_date(value)

    def get_max_date(self):
        if self.native.MaxDate == NO_MAX:
            return None
        return py_date(self.native.MaxDate)

    def set_max_date(self, value):
        self.native.MaxDate = NO_MAX if value is None else native_date(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def winforms_value_changed(self, sender, event):
        self.interface.on_change(self.interface)
