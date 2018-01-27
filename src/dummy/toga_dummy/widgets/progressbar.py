from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self._action('create ProgressBar')

    def set_value(self, value):
        self._set_value('value', value)

    def set_running(self, value):
        self._set_value('running', value)

    def set_max(self, value):
        self._set_value('max', value)
