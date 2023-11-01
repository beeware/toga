from toga.widgets.numberinput import _clean_decimal

from .base import Widget


class NumberInput(Widget):
    def create(self):
        self._action("create NumberInput")

    def get_readonly(self):
        return self._get_value("readonly", False)

    def set_readonly(self, value):
        self._set_value("readonly", value)

    def set_step(self, step):
        self._set_value("step", step)

    def set_min_value(self, value):
        self._set_value("min", value)

    def set_max_value(self, value):
        self._set_value("max", value)

    def set_value(self, value):
        self._set_value("value", value)
        self.interface.on_change()

    def get_value(self):
        value = self._get_value("value", None)
        if value is None:
            return value
        else:
            return _clean_decimal(value, self.interface.step)

    def set_on_change(self, handler):
        self._set_value("on_change", handler)

    def simulate_change(self):
        self.interface.on_change()
