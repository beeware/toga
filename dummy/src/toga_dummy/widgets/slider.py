import toga

from .base import Widget


class Slider(Widget, toga.widgets.slider.SliderImpl):
    def create(self):
        self._action("create Slider")

    def get_value(self):
        return self._get_value("value", 0)

    def set_value(self, value):
        self._set_value("value", value)

    def get_range(self):
        return self._get_value("range")

    def set_range(self, range):
        self._set_value("range", range)

    def get_tick_count(self):
        return self._get_value("tick_count", None)

    def set_tick_count(self, tick_count):
        self._set_value("tick_count", tick_count)
