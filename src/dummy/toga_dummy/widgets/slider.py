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

    def rehint(self):
        self._action('rehint Slider')

    def set_on_slide(self, handler):
        self._set_value('on_slide', handler)
