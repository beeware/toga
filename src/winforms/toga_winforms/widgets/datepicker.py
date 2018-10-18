from toga_winforms.libs import WinForms, WinDateTime
from travertino.size import at_least
import datetime

from .base import Widget


class DatePicker(Widget):
    def create(self):
        self.native = WinForms.DateTimePicker()

    def get_value(self):
        date = self.native.Text
        date = datetime.datetime.strptime(date, '%A, %B %d, %Y')
        date = date.date()
        return date

    def set_value(self, value):
        value = WinDateTime.Parse(value)
        self.native.Value = value

    def rehint(self):
        # Height of a date input is known and fixed.
        # Width must be > 200
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

