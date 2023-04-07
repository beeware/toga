from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class Label(Widget):
    def create(self):
        self._action("create Label")

    def set_alignment(self, value):
        self._set_value("alignment", value)

    def get_text(self):
        return self._get_value("text")

    def set_text(self, value):
        self._set_value("text", value)
