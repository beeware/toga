from datetime import time

from ..libs.android import R__drawable
from ..libs.android.widget import TimePickerDialog
from ..libs.android.widget import \
    TimePickerDialog__OnTimeSetListener as OnTimeSetListener
from .internal.pickers import PickerBase


class TimePicker(PickerBase):
    @classmethod
    def _get_icon(cls):
        return R__drawable.ic_menu_recent_history

    @classmethod
    def _get_hint(cls):
        return "HH:MM"

    @classmethod
    def _get_dialog_constructor(cls):
        def partial_constructor(*args, **kwargs):
            # The `True` value is for required argument `is2HourView`,
            # which is needed by Android Dialog, and needs to be last
            # However, Rubicon does not allow for kwargs,
            # so the standard partial solution would not work
            return TimePickerDialog(*args, True, **kwargs)

        return partial_constructor

    @classmethod
    def _get_dialog_listener_class(cls):
        return OnTimeSetListener

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

    def _extra_dialog_setup(self):
        pass

    def _get_update_fn(self):
        return self._dialog.updateTime

    def set_min_time(self, value):
        self.interface.factory.not_implemented("TimePicker.set_min_time()")

    def set_max_time(self, value):
        self.interface.factory.not_implemented("TimePicker.set_max_time()")
