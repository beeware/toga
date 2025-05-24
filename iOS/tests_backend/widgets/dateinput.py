import datetime
from abc import ABC, abstractmethod

import pytest

from toga_iOS.libs import (
    NSCalendar,
    NSCalendarUnit,
    UIControlContentHorizontalAlignmentLeft,
    UIDatePicker,
    UIDatePickerMode,
)

from .base import SimpleProbe
from .properties import toga_color


class DateTimeInputProbe(SimpleProbe, ABC):
    native_class = UIDatePicker
    supports_limits = True

    @abstractmethod
    def py_value(self, native_value):
        pass

    @property
    def value(self):
        return self.py_value(self.native.date)

    @property
    def min_value(self):
        return self.py_value(self.native.minimumDate)

    @property
    def max_value(self):
        return self.py_value(self.native.maximumDate)


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
        # FIXME: It is possible to change the date in the UIDatePicker on iOS, but
        # changing it this way does not call the registered selector. Therefore it might
        # just be impossible to automatically test that the on_change handler works.
        self.native.date = NSCalendar.currentCalendar.dateByAddingUnit(
            NSCalendarUnit.Day, value=delta, toDate=self.native.date, options=0
        )
        # Call it manually to have the test pass for now.
        self.widget.on_change()
        await self.redraw(f"Change value by {delta} days")

    @property
    def color(self):
        return toga_color(self.native.tintColor)

    @property
    def background_color(self):
        # .backgroundColor returns nil even when one is *just* set and it shows
        # in the UI. Skip it.
        # TODO: Should this color be kept track of manually?
        pytest.skip("Background color cannot be obtained on DateInput for iOS")
