from datetime import time

from ..libs.android import R__drawable
from ..libs.android.widget import TimePickerDialog
from ..libs.android.widget import \
    TimePickerDialog__OnTimeSetListener as OnTimeSetListener
from .internal.pickers import PickerBase, TogaPickerSetListener


class TimePickerListener(TogaPickerSetListener, OnTimeSetListener):
    pass


class TimePicker(PickerBase):
    @classmethod
    def _get_icon(cls):
        return R__drawable.ic_menu_recent_history

    @classmethod
    def _get_hint(cls):
        return "HH:MM"

    @classmethod
    def obj_to_args(cls, value):
        return value.hour, value.minute

    @classmethod
    def args_to_obj(cls, *args):
        return time(*args)

    @classmethod
    def obj_to_str(cls, value):
        return value.isoformat(timespec="minutes")

    @classmethod
    def str_to_obj(cls, value):
        return time.fromisoformat(value)

    def _get_update_fn(self):
        return self._dialog.updateTime

    def set_min_time(self, value):
        self.interface.factory.not_implemented("TimePicker.set_min_time()")

    def set_max_time(self, value):
        self.interface.factory.not_implemented("TimePicker.set_max_time()")

    def _create_dialog(self):
        self._dialog = TimePickerDialog(
            self._native_activity,
            TimePickerListener(self),
            *(self.obj_to_args(self._value) + (True,))
        )
        self._showing = True
        self._dialog.show()
