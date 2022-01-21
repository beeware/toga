from datetime import date, datetime

from ..libs.android import R__drawable
from ..libs.android.widget import DatePickerDialog
from ..libs.android.widget import \
    DatePickerDialog__OnDateSetListener as OnDateSetListener
from ._pickers import PickerBase


def _date_to_milli(value):
    if isinstance(value, str):
        value = date.fromisoformat(value)
    datetime_value = datetime.combine(value, datetime.min.time())
    timestamp = datetime_value.timestamp()
    return int(timestamp * 1000)


class DatePicker(PickerBase):
    _hint = "YYYY-MM-DD"
    _icon = R__drawable.ic_menu_my_calendar
    _to_obj_converter_class = date
    _to_str_converter_kwargs = {}
    _dialog_class = DatePickerDialog
    _update_dialog_name = "updateDate"
    _extra_dialog_setters = ("min_date", "max_date")
    _extra_dialog_args = ()
    _dialog_listener_class = OnDateSetListener

    def set_min_date(self, value):
        if value is not None and self._dialog is not None and self._showing:
            self._dialog.getDatePicker().setMinDate(_date_to_milli(value))

    def set_max_date(self, value):
        if value is not None and self._dialog is not None and self._showing:
            self._dialog.getDatePicker().setMaxDate(_date_to_milli(value))

    def _value_pack_fn(self, day, month, year):
        return (day, month + 1, year)

    def _value_unpack_fn(self, value):
        return value.year, value.month - 1, value.day
