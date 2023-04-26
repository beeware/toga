from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class Box(Widget):
    def create(self):
        self._action("create Box")
