import datetime

from toga.widgets.dateinput import MAX_DATE, MIN_DATE
from toga_web.libs import create_proxy

from .base import Widget


def py_date(native_value):
    return datetime.date.fromisoformat(native_value)


def native_date(py_date_obj):
    return py_date_obj.isoformat()


class DateInput(Widget):
    def create(self):
        self.native = self._create_native_widget("wa-input")
        self.native.type = "date"
        self.native.value = native_date(datetime.date.today())
        self.native.addEventListener("change", create_proxy(self.dom_change))

    def dom_change(self, event):
        try:
            input_date = py_date(self.native.value)
        except Exception:
            input_date = datetime.date.today()

        self.set_value(input_date)
        self.interface.on_change()

    def get_value(self):
        try:
            return py_date(self.native.value)
        except Exception:
            return datetime.date.today()

    def set_value(self, value):
        if value is None:
            value = datetime.date.today()

        min_date = self.get_min_date()
        max_date = self.get_max_date()

        if value < min_date:
            value = min_date
        elif value > max_date:
            value = max_date

        self.native.value = native_date(value)

    def set_min_date(self, value):
        self.native.min = native_date(value)

    def get_min_date(self):
        try:
            native_min = self.native.min
        except AttributeError:
            return MIN_DATE
        if native_min is None:
            return MIN_DATE
        return datetime.date.fromisoformat(str(native_min))

    def set_max_date(self, value):
        self.native.max = native_date(value)

    def get_max_date(self):
        try:
            native_max = self.native.max
        except AttributeError:
            return MAX_DATE
        if native_max is None:
            return MAX_DATE
        return datetime.date.fromisoformat(str(native_max))
