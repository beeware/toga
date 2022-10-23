import datetime

from travertino.size import at_least

from toga_winforms.libs import WinDateTime, WinForms

from .base import Widget


class DatePicker(Widget):
    def create(self):
        self.native = WinForms.DateTimePicker()

    def get_value(self):
        return datetime.datetime.strptime(self.native.Text, '%A, %B %d, %Y').date()

    def set_value(self, value):
        self.native.Value = WinDateTime(value.year, value.month, value.day)

    def set_min_date(self, value):
        if value is None:
            value = self.native.MinDateTime
        else:
            value = WinDateTime(value.year, value.month, value.day)

        self.native.MinDate = value

    def set_max_date(self, value):
        if value is None:
            value = self.native.MaxDateTime
        else:
            value = WinDateTime(value.year, value.month, value.day)

        self.native.MaxDate = value

    def rehint(self):
        # Height of a date input is known and fixed.
        # Width must be > 200
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_on_change(self, handler):
        self.native.ValueChanged += self.on_date_change

    def on_date_change(self, sender, event):
        if self.interface._on_change:
            self.interface.on_change(self.interface)
