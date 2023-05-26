import datetime

from travertino.size import at_least

from toga_winforms.libs import CultureInfo, WinDateTime, WinForms

from .base import Widget


def py_date(value):
    return datetime.datetime.strptime(
        value.ToString("yyyy-MM-ddTHH:mm:sszzz", CultureInfo.InvariantCulture),
        "%Y-%m-%dT%H:%M:%S%z",
    ).date()


class DatePicker(Widget):
    def create(self):
        self.native = WinForms.DateTimePicker()
        self.native.ValueChanged += self.winforms_value_changed

    def get_value(self):
        return py_date(self.native.Value)

    def set_value(self, value):
        self.native.Value = WinDateTime(value.year, value.month, value.day)

    def get_min_date(self):
        if self.native.MinDate == self.native.MinDateTime:
            return None
        return py_date(self.native.MinDate)

    def set_min_date(self, value):
        if value is None:
            value = self.native.MinDateTime
        else:
            value = WinDateTime(value.year, value.month, value.day)

        self.native.MinDate = value

    def get_max_date(self):
        if self.native.MaxDate == self.native.MaxDateTime:
            return None
        return py_date(self.native.MaxDate)

    def set_max_date(self, value):
        if value is None:
            value = self.native.MaxDateTime
        else:
            value = WinDateTime(value.year, value.month, value.day)

        self.native.MaxDate = value

    def rehint(self):
        # Height of a date input is known and fixed.
        # Width must be > 200
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def winforms_value_changed(self, sender, event):
        self.interface.on_change(self.interface)
