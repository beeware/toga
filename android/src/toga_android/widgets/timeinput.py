from datetime import time

from android import R
from android.app import TimePickerDialog
from java import dynamic_proxy

from toga_android.widgets.base import ContainedWidget

from .internal.pickers import PickerBase


class TimePickerListener(dynamic_proxy(TimePickerDialog.OnTimeSetListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onTimeSet(self, view, hour, minute):
        # Unlike DatePicker, TimePicker does not natively support a min or max. So the
        # dialog allows the user to select any time, and we then clip the result by
        # assigning it via the interface.
        self.impl.interface.value = time(hour, minute)


class TimeInput(PickerBase, ContainedWidget):
    @classmethod
    def _get_icon(cls):
        return R.drawable.ic_menu_recent_history

    def create(self):
        super().create()

        # Dummy initial values
        self.native.setText("00:00")
        self._min_time = time(0, 0, 0)
        self._max_time = time(23, 59, 59)

    def get_value(self):
        return time.fromisoformat(str(self.native.getText()))

    def set_value(self, value):
        self.native.setText(value.isoformat(timespec="minutes"))
        self._dialog.updateTime(value.hour, value.minute)
        self.interface.on_change()

    def get_min_time(self):
        return self._min_time

    def set_min_time(self, value):
        self._min_time = value

    def get_max_time(self):
        return self._max_time

    def set_max_time(self, value):
        self._max_time = value

    def _create_dialog(self):
        return TimePickerDialog(
            self._native_activity,
            TimePickerListener(self),
            0,  # hour (dummy initial value)
            0,  # minute
            True,  # is24HourView
        )
