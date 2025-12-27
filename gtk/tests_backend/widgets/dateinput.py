import datetime
from abc import ABC, abstractmethod

from toga_gtk.libs import GTK_VERSION, Gtk

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
        # Normally for GTK4, 236 is required but libadwaita applies
        # custom stylesheets, bloating it to 243.
        self.minimum_required_height = 243

    def py_value(self, native_value):
        if GTK_VERSION >= (4, 0, 0):
            return datetime.date(
                native_value.get_year(),
                native_value.get_month(),
                native_value.get_day_of_month(),
            )
        else:
            year, month, day = native_value
            return datetime.date(year, month + 1, day)

    async def change(self, delta):
        if GTK_VERSION >= (4, 0, 0):
            self.native.select_day(self.native.get_date().add_days(delta))

            await self.redraw(f"Change value by {delta} days")
        else:
            year, month, day = self.native.get_date()
            self.native.select_month(month=month, year=year)
            self.native.select_day(day=day + delta)

            await self.redraw(f"Change value by {delta} days")
