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

    def set_step(self, step):
        self._set_value("step", step)

    def set_min_value(self, value):
        self._set_value("min_value", value)

    def set_max_value(self, value):
        self._set_value("max_value", value)

    def get_value(self):
        return self._get_value("value", None)

    def set_value(self, value):
        self._set_value("value", value)
        self.interface.on_change(None)

    def set_on_change(self, handler):
        self._set_value("on_change", handler)

    def simulate_change(self):
        self.interface.on_change(None)
