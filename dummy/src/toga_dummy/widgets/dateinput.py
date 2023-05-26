from datetime import date

from .base import Widget


class DateInput(Widget):
    def create(self):
        self._action("create DateInput")

    def get_value(self):
        return self._get_value("value", date.today())

    def set_value(self, value):
        self._set_value("value", value)
        self.interface.on_change(None)

    def get_min_date(self):
        return self._get_value("min date", None)

    def set_min_date(self, value):
        self._set_value("min date", value)

    def get_max_date(self):
        return self._get_value("max date", None)

    def set_max_date(self, value):
        self._set_value("max date", value)

    def set_on_change(self, handler):
        self._set_value("on_change", handler)
