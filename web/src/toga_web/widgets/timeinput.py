import datetime

from toga_web.libs import create_proxy

from .base import Widget


def py_time(native_time):
    return datetime.time.fromisoformat(native_time)


def native_time(py_time):
    return py_time.strftime("%H:%M")


class TimeInput(Widget):
    def create(self):
        self._return_listener = None
        self.native = self._create_native_widget("sl-input")
        self.native.setAttribute("type", "time")

        self.set_value(datetime.datetime.now().time().strftime("%H:%M"))
        self.native.addEventListener("sl-change", create_proxy(self.on_change))

    def on_change(self, event):
        self.interface.on_change(None)

    def get_value(self):
        return py_time(self.native.value)

    def set_value(self, value):
        if value is None:
            self.native.value = ""
        self.native.value = self._format_time(value)

    def set_min_time(self, value):
        self.native.min = self._format_time(value)

    def set_max_time(self, value):
        self.native.max = self._format_time(value)

    def get_min_time(self):
        if self.native.min:
            return py_time(self.native.min)
        return datetime.time(0, 0, 0)

    def get_max_time(self):
        if self.native.max:
            return py_time(self.native.max)
        return datetime.time(23, 59, 59)

    def _format_time(self, value):
        if isinstance(value, str):
            value = native_time(py_time(value))
        if isinstance(value, datetime.time):
            value = native_time(value)
        return value
