from datetime import time

from System import ArgumentOutOfRangeException
from System.Windows.Forms import DateTimePickerFormat

from .dateinput import DateTimeInputProbe


class TimeInputProbe(DateTimeInputProbe):
    supports_seconds = True

    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.Format == DateTimePickerFormat.Time
        assert self.native.ShowUpDown

    def py_value(self, native_value):
        assert (native_value.Year, native_value.Month, native_value.Day) == (1970, 1, 1)
        return time(native_value.Hour, native_value.Minute, native_value.Second)

    async def change(self, delta):
        try:
            self.native.Value = self.native.Value.AddMinutes(delta)
        except ArgumentOutOfRangeException:
            pass
        await self.redraw(f"Change value by {delta} minutes")
