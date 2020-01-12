from .base import Widget


class Divider(Widget):
    def create(self):
        self._action('create Divider')

    def rehint(self):
        self._action('rehint Divider')

    def set_direction(self, value):
        self._set_value('direction', value)
