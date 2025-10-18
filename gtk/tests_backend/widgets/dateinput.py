import datetime
from abc import ABC, abstractmethod

from toga_gtk.libs import Gtk

from .base import SimpleProbe


class DateTimeInputProbe(SimpleProbe, ABC):
    native_class = Gtk.Calendar
    supports_limits = True

    def __init__(self, widget):
        super().__init__(widget)

    @abstractmethod
    def py_value(self, native_value):
        pass

    @property
    def value(self):
        return self.py_value(self.native.get_date())

    @property
    def min_value(self):
        return self.py_value(self.native.minDate)

    @property
    def max_value(self):
        return self.py_value(self.native.maxDate)


class DateInputProbe(DateTimeInputProbe):
    def __init__(self, widget):
        super().__init__(widget)
        self.minimum_required_height = 236

    def py_value(self, native_value):
        year, month, day = native_value
        return datetime.date(year, month + 1, day)

    async def change(self, delta):
        year, month, day = self.native.get_date()
        self.native.select_month(month=month, year=year)
        self.native.select_day(day=day + delta)

        await self.redraw(f"Change value by {delta} days")
