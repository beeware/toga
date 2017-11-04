from .base import Widget


class NumberInput(Widget):
    def create(self):
        self._action('create NumberInput')

    def set_value(self, value):
        self._set_value('value', value)

    def get_value(self):
        return self._get_value('value')
