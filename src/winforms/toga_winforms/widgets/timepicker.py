import datetime

from travertino.size import at_least

from toga_winforms.libs import WinDateTime, WinForms

from .base import Widget


class TimePicker(Widget):
    def create(self):
        self.native = WinForms.DateTimePicker()
        self.native.ValueChanged += self.winforms_value_changed
        self.native.Format = WinForms.DateTimePickerFormat.Time
        self.native.ShowUpDown = True

    def get_value(self):
        time = datetime.datetime.strptime(self.native.Text, '%I:%M:%S %p').time()
        return time

    def set_value(self, value):
        value = WinDateTime.Parse(value)
        self.native.Value = value

    def set_min_time(self, value):
        if value is None:
            value = str(self.native.MinDateTime)
        value = WinDateTime.Parse(value)
        if self.native.Value < value:
            self.native.Value = value

    def set_max_time(self, value):
        if value is None:
            value = str(self.native.MaxDateTime)
        value = WinDateTime.Parse(value)
        if self.native.Value > value:
            self.native.Value = value

    def rehint(self):
        # Height of a date input is known and fixed.
        # Width must be > 100
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_on_change(self, handler):
        pass

    def winforms_value_changed(self, sender, event):
        # Since there is no native option to set a min or max time, calling min/max to validate on each change.
        self.set_max_time(self.interface.max_time)
        self.set_min_time(self.interface.min_time)
        if self.interface._on_change:
            self.interface.on_change(self.interface)
