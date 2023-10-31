import datetime

from toga_web.libs import create_proxy

from .base import Widget


def py_date(native_date):
    return datetime.datetime.strptime(native_date, "%m/%d/%y").date()


class DateInput(Widget):
    def create(self):
        self._return_listener = None
        self.native = self._create_native_widget("sl-input")
        self.native.setAttribute("type", "date")
        self.set_value(datetime.date.today().strftime("%m/%d/%y"))
        self.native.addEventListener("sl-change", create_proxy(self.on_change))

    def get_value(self):
        return py_date(self.native.value)

    def set_value(self, value):
        if value is None:
            self.native.value = ""
        self.native.value = value

    def on_change(self, event):
        self.interface.on_change(None)

    def get_min_date(self):
        if self.native.min:
            return self.native.min
        return datetime.date(1800, 1, 1)

    def get_max_date(self):
        if self.native.max:
            return self.native.max
        return datetime.date(8999, 12, 31)

    def set_min_date(self, value):
        self.native.min = value

    def set_max_date(self, value):
        self.native.max = value
