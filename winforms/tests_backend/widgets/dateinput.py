import datetime

from System.Windows.Forms import DateTimePicker, DateTimePickerFormat

from .base import SimpleProbe


def py_date(native_date):
    return datetime.date(native_date.Year, native_date.Month, native_date.Day)


class DateInputProbe(SimpleProbe):
    native_class = DateTimePicker
    background_supports_alpha = False
    fixed_height = 18

    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.Format == DateTimePickerFormat.Long
        assert not self.native.ShowUpDown

    @property
    def value(self):
        return py_date(self.native.Value)

    @property
    def min_date(self):
        return py_date(self.native.MinDate)

    @property
    def max_date(self):
        return py_date(self.native.MaxDate)

    async def change(self):
        self.widget.focus()
        await self.type_character("<up>")
