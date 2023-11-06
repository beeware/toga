from abc import ABC, abstractmethod
from datetime import date

from System import ArgumentOutOfRangeException
from System.Windows.Forms import DateTimePicker, DateTimePickerFormat

from .base import SimpleProbe


class DateTimeInputProbe(SimpleProbe, ABC):
    native_class = DateTimePicker
    background_supports_alpha = False
    fixed_height = 23
    supports_limits = True

    @abstractmethod
    def py_value(self, native_value):
        pass

    @property
    def value(self):
        return self.py_value(self.native.Value)

    @property
    def min_value(self):
        return self.py_value(self.native.MinDate)

    @property
    def max_value(self):
        return self.py_value(self.native.MaxDate)


class DateInputProbe(DateTimeInputProbe):
    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.Format == DateTimePickerFormat.Long
        assert not self.native.ShowUpDown

    def py_value(self, native_value):
        return date(native_value.Year, native_value.Month, native_value.Day)

    async def change(self, delta):
        try:
            self.native.Value = self.native.Value.AddDays(delta)
        except ArgumentOutOfRangeException:
            pass
        await self.redraw(f"Change value by {delta} days")
