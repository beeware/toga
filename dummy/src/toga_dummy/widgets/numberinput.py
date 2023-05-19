from decimal import Decimal

from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class NumberInput(Widget):
    def create(self):
        self._action("create NumberInput")

    def get_readonly(self):
        return self._get_value("readonly", False)

    def set_readonly(self, value):
        self._set_value("readonly", value)

    def get_step(self):
        return self._get_value("step", Decimal(1))

    def set_step(self, step):
        self._set_value("step", step)

    def get_min_value(self):
        return self._set_value("min value", None)

    def set_min_value(self, value):
        self._set_value("min value", value)

    def get_max_value(self):
        return self._set_value("max value", None)

    def set_max_value(self, value):
        self._set_value("max value", value)

    def get_value(self):
        return self._get_value("value", None)

    def set_value(self, value):
        self._set_value("value", value)

    def set_on_change(self, handler):
        self._set_value("on_change", handler)
