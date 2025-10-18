import datetime

from toga_web.libs import create_proxy

from .base import Widget


def py_time(native_time):
    if isinstance(native_time, datetime.datetime):
        time = native_time.time()
    elif isinstance(native_time, str):
        time = datetime.time.fromisoformat(native_time)
    else:
        time = datetime.datetime.now().time()

    return time.replace(microsecond=0)


def native_time(py_time):
    if isinstance(py_time, datetime.datetime):
        time = py_time.time()
    else:
        time = py_time

    return time.replace(microsecond=0).isoformat()


class TimeInput(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-input")
        self.native.setAttribute("step", "1")  # force seconds to show
        self.native.type = "time"
        self.native.value = native_time(datetime.datetime.now())
        self.native.addEventListener("sl-change", create_proxy(self.dom_sl_change))

    def dom_sl_change(self, event):
        try:
            input_time = py_time(self.native.value)
        except Exception:
            input_time = datetime.datetime.now().time().replace(microsecond=0)

        self.set_value(input_time)
        self.interface.on_change()

    def get_value(self):
        try:
            return py_time(self.native.value)
        except Exception:
            return datetime.datetime.now().time().replace(microsecond=0)

    def set_value(self, value):
        if value is None or not isinstance(value, datetime.time):
            value = datetime.datetime.now().time().replace(microsecond=0)

        min_time = self.get_min_time()
        max_time = self.get_max_time()

        if value < min_time:
            value = min_time
        elif value > max_time:
            value = max_time
        self.native.value = native_time(value)

    def get_min_time(self):
        min_value = self.native.min if self.native.min else datetime.time(0, 0, 0)
        return py_time(min_value)

    def set_min_time(self, value):
        self.native.min = native_time(value)

    def get_max_time(self):
        max_value = self.native.max if self.native.max else datetime.time(23, 59, 59)
        return py_time(max_value)

    def set_max_time(self, value):
        self.native.max = native_time(value)
