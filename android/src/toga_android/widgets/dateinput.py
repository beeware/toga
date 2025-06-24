from datetime import date, datetime, time

from android import R
from android.app import DatePickerDialog
from java import dynamic_proxy

from toga_android.widgets.base import ContainedWidget

from .internal.pickers import PickerBase


def py_date(native_date):
    return date.fromtimestamp(native_date / 1000)


def native_date(py_date):
    return int(datetime.combine(py_date, time.min).timestamp() * 1000)


class DatePickerListener(dynamic_proxy(DatePickerDialog.OnDateSetListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onDateSet(self, view, year, month_0, day):
        # It should be impossible for the dialog to return an out-of-range value in
        # normal use, but it can happen in the testbed, so go via the interface to clip
        # the value.
        self.impl.interface.value = date(year, month_0 + 1, day)


class DateInput(PickerBase, ContainedWidget):
    @classmethod
    def _get_icon(cls):
        return R.drawable.ic_menu_my_calendar

    def create(self):
        super().create()
        self.native.setText("2000-01-01")  # Dummy initial value

    def get_value(self):
        return date.fromisoformat(str(self.native.getText()))

    def set_value(self, value):
        self.native.setText(value.isoformat())
        self._dialog.updateDate(value.year, value.month - 1, value.day)
        self.interface.on_change()

    def get_min_date(self):
        return py_date(self._picker.getMinDate())

    def set_min_date(self, value):
        self._picker.setMinDate(native_date(value))

    def get_max_date(self):
        return py_date(self._picker.getMaxDate())

    def set_max_date(self, value):
        self._picker.setMaxDate(native_date(value))

    def _create_dialog(self):
        return DatePickerDialog(
            self._native_activity,
            DatePickerListener(self),
            2000,  # year (dummy initial value)
            0,  # month (0 = January)
            1,  # day
        )

    @property
    def _picker(self):
        return self._dialog.getDatePicker()
