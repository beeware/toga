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
        return datetime.datetime.strptime(self.native.Text, '%I:%M:%S %p').time()

    def set_value(self, value):
        # Jan 1 1970 is a dummy date; we don't need the date component
        self.native.Value = WinDateTime(1970, 1, 1, value.hour, value.minute, value.second)

    def set_min_time(self, value):
        if value is None:
            value = self.native.MinDateTime
        else:
            # Jan 1 1970 is a dummy date; we don't need the date component
            value = WinDateTime(1970, 1, 1, value.hour, value.minute, value.second)
        if self.native.Value < value:
            self.native.Value = value

    def set_max_time(self, value):
        if value is None:
            value = self.native.MaxDateTime
        else:
            # Jan 1 1970 is a dummy date; we don't need the date component
            value = WinDateTime(1970, 1, 1, value.hour, value.minute, value.second)

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
