from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class Switch(Widget):
    def create(self):
        self._action("create Switch")

    def get_text(self):
        return self._get_value("text")

    def set_text(self, text):
        self._set_value("text", text)

    def get_value(self):
        return self._get_value("value")

    def set_value(self, value):
        old_value = self._get_value("value", None)
        self._set_value("value", value)
        if value != old_value:
            self.interface.on_change(None)

    def simulate_toggle(self):
        self.interface.on_change(None)
