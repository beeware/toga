from datetime import time

from ..libs.android import R__drawable
from ..libs.android.widget import TimePickerDialog
from ..libs.android.widget import \
    TimePickerDialog__OnTimeSetListener as OnTimeSetListener
from ._pickers import PickerBase


class TimePicker(PickerBase):
    _hint = "HH:MM"
    _icon = R__drawable.ic_menu_recent_history
    _to_obj_converter_class = time
    _to_str_converter_kwargs = {"timespec": "minutes"}
    _dialog_class = TimePickerDialog
    _update_dialog_name = "updateTime"
    _extra_dialog_setters = ("min_time", "max_time")
    _extra_dialog_args = (True,)
    _dialog_listener_class = OnTimeSetListener

    def set_min_time(self, value):
        self.interface.factory.not_implemented("TimePicker.set_min_time()")

    def set_max_time(self, value):
        self.interface.factory.not_implemented("TimePicker.set_max_time()")

    def _value_pack_fn(self, hour, minute):
        return (hour, minute)

    def _value_unpack_fn(self, value):
        return value.hour, value.minute
