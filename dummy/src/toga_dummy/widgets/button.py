from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class Button(Widget):
    def create(self):
        self._action("create Button")

    def get_text(self):
        return self._get_value("text")

    def set_text(self, text):
        self._set_value("text", text)

    def simulate_press(self):
        self.interface.on_press(None)
