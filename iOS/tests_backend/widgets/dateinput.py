import datetime

import pytest

from toga_iOS.libs import (
    NSCalendar,
    NSCalendarUnit,
    UIControlContentHorizontalAlignmentLeft,
    UIControlEventValueChanged,
    UIDatePicker,
    UIDatePickerMode,
)

from .base import SimpleProbe


class DateInputProbe(SimpleProbe):
    native_class = UIDatePicker
    supports_limits = True

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
        # It is possible to change the date in the UIDatePicker on iOS, but
        # this requires us to manually call the "value changed".
        self.native.date = NSCalendar.currentCalendar.dateByAddingUnit(
            NSCalendarUnit.Day, value=delta, toDate=self.native.date, options=0
        )
        # Call it manually to have the test pass for now.
        self.native.sendActionsForControlEvents(UIControlEventValueChanged)
        await self.redraw(f"Change value by {delta} days")

    @property
    def color(self):
        pytest.xfail("Color is not implemented for DateInput on iOS")

    @property
    def background_color(self):
        pytest.xfail(
            "Background color is not readable on the native API for DateInput on iOS"
        )

    @property
    def value(self):
        return self.py_value(self.native.date)

    @property
    def min_value(self):
        return self.py_value(self.native.minimumDate)

    @property
    def max_value(self):
        return self.py_value(self.native.maximumDate)
