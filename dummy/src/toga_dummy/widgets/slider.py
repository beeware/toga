from .base import Widget


class Slider(Widget):
    def create(self):
        self._action("create Slider")

    def get_value(self):
        return self._get_value("value")

    def set_value(self, value):
        self._set_value("value", value)

    def set_range(self, range):
        self._set_value("range", range)

    def set_tick_count(self, tick_count):
        self._set_value("tick_count", tick_count)
