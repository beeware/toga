import datetime

from toga_cocoa.libs import (
    NSApplication,
    NSCalendar,
    NSCalendarUnit,
    NSDatePickerElementFlags,
)

from .dateinput import DateTimeInputProbe


class TimeInputProbe(DateTimeInputProbe):
    supports_seconds = True

    def __init__(self, widget):
        super().__init__(widget)
        assert (
            self.native.datePickerElements == NSDatePickerElementFlags.HourMinuteSecond
        )

    def py_value(self, native_value):
        components = NSCalendar.currentCalendar.components(
            NSCalendarUnit.Hour | NSCalendarUnit.Minute | NSCalendarUnit.Second,
            fromDate=native_value,
        )
        return datetime.time(components.hour, components.minute, components.second)

    async def change(self, delta):
        # It is possible to change the time in the NSDatePicker on macOS, but
        # this requires us to manually call the "value changed".
        self.native.dateValue = NSCalendar.currentCalendar.dateByAddingUnit(
            NSCalendarUnit.Minute, value=delta, toDate=self.native.dateValue, options=0
        )
        # Call it manually to have the test pass for now.
        NSApplication.sharedApplication.sendAction(
            self.native.action, to=self.native.target, from__=self.native
        )
        await self.redraw(f"Change value by {delta} minutes")
