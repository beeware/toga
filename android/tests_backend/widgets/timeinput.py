import re
from datetime import time

from android import R
from android.widget import TimePicker

from .base import find_view_by_type
from .dateinput import DateTimeInputProbe


class TimeInputProbe(DateTimeInputProbe):
    supports_limits = False
    supports_seconds = False

    @property
    def value(self):
        text = str(self.native.getText())
        assert re.fullmatch(r"\d{2}:\d{2}", text)
        return time.fromisoformat(text)

    async def _check_dialog_value(self):
        dialog_value = time(
            self._picker.getCurrentHour(), self._picker.getCurrentMinute()
        )
        assert dialog_value == self.value

    async def _change_dialog_value(self, delta):
        new_minute = self._picker.getCurrentMinute() + delta
        if not (0 <= new_minute <= 59):
            raise ValueError("Cannot cross minute boundaries")

        self._dialog.updateTime(self._picker.getCurrentHour(), new_minute)
        await self.redraw(f"Change value by {delta} minutes")

    @property
    def _picker(self):
        picker = find_view_by_type(self._dialog.findViewById(R.id.content), TimePicker)
        assert picker is not None
        assert picker.is24HourView()
        return picker
