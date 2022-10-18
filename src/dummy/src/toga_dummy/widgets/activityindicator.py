from .base import Widget


class ActivityIndicator(Widget):

    def create(self):
        self._action('create ActivityIndicator')

    def start(self):
        self._action('start ActivityIndicator')

    def stop(self):
        self._action('stop ActivityIndicator')
