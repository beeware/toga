import datetime
from abc import ABC, abstractmethod

from toga_iOS.libs import (
    NSCalendar,
    NSCalendarUnit,
    UIControlContentHorizontalAlignmentLeft,
    UIDatePicker,
    UIDatePickerMode,
)

from .base import SimpleProbe


class DateTimeInputProbe(SimpleProbe, ABC):
    native_class = UIDatePicker
    supports_limits = True

    @abstractmethod
    def py_value(self, native_value):
        pass

    @property
    def value(self):
        return self.py_value(self.native.value)

    @property
    def min_value(self):
        return self.py_value(self.native.min)

    @property
    def max_value(self):
        return self.py_value(self.native.max)


class DateInputProbe(DateTimeInputProbe):
    def __init__(self, widget):
        super().__init__(widget)
        assert (
            self.native.contentHorizontalAlignment
            == UIControlContentHorizontalAlignmentLeft
        )
        assert self.native.datePickerMode == UIDatePickerMode.Date

    def py_value(self, native_value):
        components = NSCalendar.currentCalendar.components(
            NSCalendarUnit(
                NSCalendarUnit.Year.value
                | NSCalendarUnit.Month.value
                | NSCalendarUnit.Day.value
            ),
            fromDate=native_value,
        )
        return datetime.date(components.year, components.month, components.day)

    async def change(self, delta):
        try:
            calendar = NSCalendar.currentCalendar()
            new_date = calendar.dateByAddingUnit(
                NSCalendarUnit.Day, value=1, toDate=self.native.date, options=[]
            )
            self.native.date = self.py_value(new_date)
        # TODO: What to except here?
        except Exception:
            pass
        await self.redraw(f"Change value by {delta} days")
