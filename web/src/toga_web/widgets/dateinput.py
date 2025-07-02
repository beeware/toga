import datetime

from toga_web.libs import create_proxy

from .base import Widget


def py_date(native_value):
    return datetime.date.fromisoformat(native_value)


def native_date(py_date_obj):
    return py_date_obj.isoformat()


class DateInput(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-input")
        self.native.type = "date"
        self.native.value = native_date(datetime.date.today())
        self.native.addEventListener("sl-change", create_proxy(self.dom_sl_change))

    def dom_sl_change(self, event):
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
        if self.native.min is None:
            return datetime.date(1800, 1, 1)
        return datetime.date.fromisoformat(str(self.native.min))

    def set_max_date(self, value):
        self.native.max = native_date(value)

    def get_max_date(self):
        if self.native.max is None:
            return datetime.date(8999, 12, 31)
        return datetime.date.fromisoformat(str(self.native.max))
