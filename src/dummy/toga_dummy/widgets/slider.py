from .base import Widget


class Slider(Widget):
    def create(self):
        self._action('create Slider')

    def get_value(self):
        return self._get_value('value')

    def set_value(self, value):
        self._set_value('value', value)

    def set_range(self, range):
        self._set_value('range', range)

    def set_tick_count(self, tick_count):
        self._set_value('tick_count', tick_count)

    def rehint(self):
        self._action('rehint Slider')

    def set_on_change(self, handler):
        self._set_value('on_change', handler)

    def set_on_press(self, handler):
        self._set_value('on_press', handler)

    def set_on_release(self, handler):
        self._set_value('on_press', handler)
