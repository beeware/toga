import datetime
from abc import ABC, abstractmethod

from toga.colors import TRANSPARENT
from toga_cocoa.libs import (
    NSApplication,
    NSCalendar,
    NSCalendarUnit,
    NSColor,
    NSDatePicker,
    NSDatePickerElementFlags,
)

from .base import SimpleProbe
from .properties import toga_color


class DateTimeInputProbe(SimpleProbe, ABC):
    native_class = NSDatePicker
    supports_limits = True

    def __init__(self, widget):
        super().__init__(widget)

    @abstractmethod
    def py_value(self, native_value):
        pass

    @property
    def value(self):
        return self.py_value(self.native.dateValue)

    @property
    def min_value(self):
        return self.py_value(self.native.minDate)

    @property
    def max_value(self):
        return self.py_value(self.native.maxDate)

    @property
    def color(self):
        if self.native.textColor == NSColor.controlTextColor:
            return None
        else:
            return toga_color(self.native.textColor)

    @property
    def background_color(self):
        if self.native.backgroundColor == NSColor.controlBackgroundColor:
            assert self.native.isBezeled()
            assert not self.native.drawsBackground
            return None
        elif self.native.drawsBackground:
            # Shouldn't bezel in this case, as it breaks
            # light mode.
            assert not self.native.isBezeled()
            # None as a background color is misconfigured, and produces
            # incorrect results visually in dark mode.
            assert self.native.backgroundColor is not None
            # If drawing with default controlBackgroundColor, drawsBackground
            # should be false, as it will be handled by the bezel.
            assert self.native.backgroundColor != NSColor.controlBackgroundColor
            return toga_color(self.native.backgroundColor)
        else:
            assert not self.native.isBezeled()
            return TRANSPARENT


class DateInputProbe(DateTimeInputProbe):
    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.datePickerElements == NSDatePickerElementFlags.YearMonthDay

    def py_value(self, native_value):
        components = NSCalendar.currentCalendar.components(
            NSCalendarUnit.Year | NSCalendarUnit.Month | NSCalendarUnit.Day,
            fromDate=native_value,
        )
        return datetime.date(components.year, components.month, components.day)

    async def change(self, delta):
        # It is possible to change the date in the NSDatePicker on macOS, but
        # this requires us to manually call the "value changed".
        self.native.setDateValue(
            NSCalendar.currentCalendar.dateByAddingUnit(
                NSCalendarUnit.Day, value=delta, toDate=self.native.dateValue, options=0
            )
        )
        # Call it manually to have the test pass for now.
        NSApplication.sharedApplication.sendAction(
            self.native.action, to=self.native.target, from__=self.native
        )
        await self.redraw(f"Change value by {delta} days")
