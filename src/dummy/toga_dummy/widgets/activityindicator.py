from .base import Widget


class ActivityIndicator(Widget):

    def create(self):
        self._action('create ActivityIndicator')

    def set_hide_when_stopped(self, value):
        self._set_value('hide_when_stopped', value)

    def start(self):
        self._action('start ActivityIndicator')

    def stop(self):
        self._action('stop ActivityIndicator')
