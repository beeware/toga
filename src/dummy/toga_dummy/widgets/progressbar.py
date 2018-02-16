from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self._action('create ProgressBar')

    def set_value(self, value):
        self._set_value('value', value)

    def set_max(self, value):
        self._set_value('max', value)

    def start(self):
        self._action('start')

    def stop(self):
        self._action('stop')
