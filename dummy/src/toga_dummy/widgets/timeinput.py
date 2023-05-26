from datetime import datetime

from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class TimeInput(Widget):
    def create(self):
        self._action("create TimeInput")

    def get_value(self):
        return self._get_value("value", datetime.now().time())

    def set_value(self, value):
        self._set_value("value", value)
        self.interface.on_change(None)

    def get_min_time(self):
        return self._get_value("min time", None)

    def set_min_time(self, value):
        self._set_value("min time", value)

    def get_max_time(self):
        return self._get_value("max time", None)

    def set_max_time(self, value):
        self._set_value("max time", value)
