import re
from datetime import time

from pytest import xfail

from android import R as android_R
from android.view import ViewGroup
from android.widget import TimePicker

from .dateinput import DateTimeInputProbe


def findViewByType(root, cls):
    if isinstance(root, cls):
        return root
    if isinstance(root, ViewGroup):
        for i in range(root.getChildCount()):
            result = findViewByType(root.getChildAt(i), cls)
            if result is not None:
                return result
    return None


class TimeInputProbe(DateTimeInputProbe):
    supports_seconds = False

    @property
    def value(self):
        text = str(self.native.getText())
        assert re.fullmatch(r"\d{2}:\d{2}", text)
        return time.fromisoformat(text)

    @property
    def min_value(self):
        xfail("This backend doesn't support min/max limits")

    @property
    def max_value(self):
        xfail("This backend doesn't support min/max limits")

    async def _check_dialog_value(self):
        dialog_value = time(
            self._picker.getCurrentHour(), self._picker.getCurrentMinute()
        )
        assert dialog_value == self.value

    async def _change_dialog_value(self):
        next_minute = (self._picker.getCurrentMinute() + 1) % 60
        self._dialog.updateTime(self._picker.getCurrentHour(), next_minute)
        await self.redraw("Increment minute")

    @property
    def _picker(self):
        picker = findViewByType(
            self._dialog.findViewById(android_R.id.content), TimePicker
        )
        assert picker is not None
        assert picker.is24HourView()
        return picker
