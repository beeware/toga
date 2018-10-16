from toga_winforms.libs import WinForms, HorizontalTextAlignment
from travertino.size import at_least

from .base import Widget


class DatePicker(Widget):
    def create(self):
        self.native = WinForms.DateTimePicker()

    def get_value(self):
        return self.native.Value

    def rehint(self):
        # Height of a date input is known and fixed.
        # Width must be > 200
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

