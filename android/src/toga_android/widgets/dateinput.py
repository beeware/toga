from datetime import date, datetime, time

from ..libs.android import R__drawable
from ..libs.android.widget import (
    DatePickerDialog,
    DatePickerDialog__OnDateSetListener as OnDateSetListener,
)
from .internal.pickers import PickerBase

NO_MIN = date(1799, 1, 1)
NO_MAX = date(9999, 1, 1)


def py_date(native_date):
    return date.fromtimestamp(native_date / 1000)


def native_date(py_date):
    return int(datetime.combine(py_date, time.min).timestamp() * 1000)


class DatePickerListener(OnDateSetListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onDateSet(self, view, year, month_0, day):
        self.impl.set_value(date(year, month_0 + 1, day))


class DateInput(PickerBase):
    @classmethod
    def _get_icon(cls):
        return R__drawable.ic_menu_my_calendar

    def create(self):
        super().create()
        self.native.setText("1970-01-01")  # Dummy value used during initialization

    def get_value(self):
        return date.fromisoformat(str(self.native.getText()))

    def set_value(self, value):
        self.native.setText(value.isoformat())
        self._dialog.updateDate(value.year, value.month - 1, value.day)
        self.interface.on_change(None)

    def get_min_date(self):
        result = py_date(self._picker.getMinDate())
        return None if (result == NO_MIN) else result

    def set_min_date(self, value):
        self._picker.setMinDate(native_date(NO_MIN if value is None else value))

    def get_max_date(self):
        result = py_date(self._picker.getMaxDate())
        return None if (result == NO_MAX) else result

    def set_max_date(self, value):
        self._picker.setMaxDate(native_date(NO_MAX if value is None else value))

    def _create_dialog(self):
        return DatePickerDialog(
            self._native_activity,
            DatePickerListener(self),
            2000,  # year
            0,  # month (0 = January)
            1,  # day
        )

    @property
    def _picker(self):
        return self._dialog.getDatePicker()
