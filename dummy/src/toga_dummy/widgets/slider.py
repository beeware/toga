import toga

from .base import Widget


class Slider(Widget, toga.widgets.slider.SliderImpl):
    def create(self):
        self._action("create Slider")

    def get_value(self):
        return self._get_value("value", 0)

    def set_value(self, value):
        self._set_value("value", value)

    def get_min(self):
        return self._get_value("min", 0)

    def set_min(self, value):
        self._set_value("min", value)

    def get_max(self):
        return self._get_value("max", 0)

    def set_max(self, value):
        self._set_value("max", value)

    def get_tick_count(self):
        return self._get_value("tick_count", None)

    def set_tick_count(self, tick_count):
        self._set_value("tick_count", tick_count)
