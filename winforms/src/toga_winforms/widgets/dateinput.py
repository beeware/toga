import datetime

from travertino.size import at_least

from toga_winforms.libs import WinDateTime, WinForms

from .base import Widget


class DateInput(Widget):
    def create(self):
        self.native = WinForms.DateTimePicker()
        self.native.ValueChanged += self.winforms_value_changed

    def get_value(self):
        return datetime.date(
            self.native.Value.Year, self.native.Value.Month, self.native.Value.Day
        )

    def set_value(self, value):
        self.native.Value = WinDateTime(value.year, value.month, value.day)

    def get_min_date(self):
        if self.native.MinDate == self.native.MinDateTime:
            return None
        return datetime.date(
            self.native.MinDate.Year, self.native.MinDate.Month, self.native.MinDate.Day
        )

    def set_min_date(self, value):
        if value is None:
            value = self.native.MinDateTime
        else:
            value = WinDateTime(value.year, value.month, value.day)

        self.native.MinDate = value

    def get_max_date(self):
        if self.native.MaxDate == self.native.MaxDateTime:
            return None
        return datetime.date(
            self.native.MaxDate.Year, self.native.MaxDate.Month, self.native.MaxDate.Day
        )

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
