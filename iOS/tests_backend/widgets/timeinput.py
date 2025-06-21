import datetime

from toga_iOS.libs import (
    NSCalendar,
    NSCalendarUnit,
    UIControlEventValueChanged,
    UIDatePickerMode,
)

from .dateinput import DateTimeInputProbe


class TimeInputProbe(DateTimeInputProbe):
    supports_seconds = False

    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.datePickerMode == UIDatePickerMode.Time

    def py_value(self, native_value):
        components = NSCalendar.currentCalendar.components(
            NSCalendarUnit.Hour | NSCalendarUnit.Minute | NSCalendarUnit.Second,
            fromDate=native_value,
        )
        return datetime.time(components.hour, components.minute, components.second)

    async def change(self, delta):
        # It is possible to change the time in the UIDatePicker on iOS, but
        # this requires us to manually call the "value changed".
        self.native.date = NSCalendar.currentCalendar.dateByAddingUnit(
            NSCalendarUnit.Minute, value=delta, toDate=self.native.date, options=0
        )
        # Call it manually to have the test pass for now.
        self.native.sendActionsForControlEvents(UIControlEventValueChanged)
        await self.redraw(f"Change value by {delta} minutes")
