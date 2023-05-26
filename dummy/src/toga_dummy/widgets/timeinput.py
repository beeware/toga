from datetime import datetime

from .base import Widget


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

    def set_on_change(self, handler):
        self._set_value("on_change", handler)
