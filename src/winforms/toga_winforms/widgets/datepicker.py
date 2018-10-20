from toga_winforms.libs import WinForms, WinDateTime
from travertino.size import at_least
import datetime

from .base import Widget


class DatePicker(Widget):
    def create(self):
        self.native = WinForms.DateTimePicker()

    def get_value(self):
        date = datetime.datetime.strptime(self.native.Text, '%A, %B %d, %Y').date()
        return date

    def set_value(self, value):
        value = WinDateTime.Parse(value)
        self.native.Value = value

    def set_min_date(self, value):
        value = WinDateTime.Parse(value)
        self.native.MinDate = value

    def set_max_date(self, value):
        value = WinDateTime.Parse(value)
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
