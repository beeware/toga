from datetime import date, datetime

from ..libs.android import R__drawable
from ..libs.android.widget import DatePickerDialog
from ..libs.android.widget import \
    DatePickerDialog__OnDateSetListener as OnDateSetListener
from .internal.pickers import PickerBase


class DatePicker(PickerBase):
    @classmethod
    def _get_icon(cls):
        return R__drawable.ic_menu_my_calendar

    @classmethod
    def _get_hint(cls):
        return "YYYY-MM-DD"

    @classmethod
    def _get_dialog_constructor(cls):
        return DatePickerDialog

    @classmethod
    def _get_dialog_listener_class(cls):
        return OnDateSetListener

    @classmethod
    def obj_to_args(cls, value):
        return value.year, value.month - 1, value.day

    @classmethod
    def args_to_obj(cls, *args):
        day, month, year = args
        return date(day, month + 1, year)

    @classmethod
    def obj_to_str(cls, value):
        return value.isoformat()

    @classmethod
    def str_to_obj(cls, value):
        return date.fromisoformat(value)

    def _extra_dialog_setup(self):
        self.set_min_date(self.interface._min_date)
        self.set_max_date(self.interface._max_date)

    def _get_update_fn(self):
        return self._dialog.updateDate

    def set_min_date(self, value):
        if value is not None and self._dialog is not None and self._showing:
            self._dialog.getDatePicker().setMinDate(self._date_to_milli(value))

    def set_max_date(self, value):
        if value is not None and self._dialog is not None and self._showing:
            self._dialog.getDatePicker().setMaxDate(self._date_to_milli(value))

    @classmethod
    def _date_to_milli(cls, value):
        if isinstance(value, str):
            value = date.fromisoformat(value)
        datetime_value = datetime.combine(value, datetime.min.time())
        timestamp = datetime_value.timestamp()
        return int(timestamp * 1000)
