import datetime
from decimal import ROUND_UP

from toga_web.libs import create_proxy

from .base import Widget


def py_date(native_date):
    if not native_date:
        return datetime.date.today()
    return datetime.date.fromisoformat(native_date)


def native_date(py_value):
    return py_value.isoformat()


class DateInput(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-input")
        self.native.setAttribute("type", "date")
        self.native.addEventListener("sl-change", create_proxy(self.dom_value_changed))

    def get_value(self):
        return py_date(self.native.value)

    def set_value(self, value):
        self.native.value = native_date(value)

    def get_min_date(self):
        min_attr = self.native.getAttribute("min")
        return py_date(min_attr) if min_attr else datetime.date(1800, 1, 1)

    def set_min_date(self, value):
        self.native.setAttribute("min", native_date(value))

    def get_max_date(self):
        max_attr = self.native.getAttribute("max")
        return py_date(max_attr) if max_attr else datetime.date(8999, 12, 31)

    def set_max_date(self, value):
        self.native.setAttribute("max", native_date(value))

    def rehint(self):
        height = self.native.offsetHeight or 40
        self.interface.intrinsic.height = self.scale_out(height, ROUND_UP)

    def dom_value_changed(self, event):
        self.interface.on_change(None)
