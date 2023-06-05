from abc import ABC, abstractmethod
from datetime import date

from System.Windows.Forms import DateTimePicker, DateTimePickerFormat

from .base import SimpleProbe


class DateTimeInputProbe(SimpleProbe, ABC):
    native_class = DateTimePicker
    background_supports_alpha = False
    fixed_height = 18

    @abstractmethod
    def py_value(self, native_value):
        pass

    @property
    def value(self):
        return self.py_value(self.native.Value)

    @property
    def min_value(self):
        if self.native.MinDate.Year < 1800:
            return None
        else:
            return self.py_value(self.native.MinDate)

    @property
    def max_value(self):
        if self.native.MaxDate.Year > 9000:
            return None
        else:
            return self.py_value(self.native.MaxDate)

    async def change(self):
        self.widget.focus()
        await self.type_character("<up>")


class DateInputProbe(DateTimeInputProbe):
    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.Format == DateTimePickerFormat.Long
        assert not self.native.ShowUpDown

    def py_value(self, native_value):
        return date(native_value.Year, native_value.Month, native_value.Day)
