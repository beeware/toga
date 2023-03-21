from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self._action("create ActivityIndicator")
        self._running = False

    def is_running(self):
        return self._running

    def start(self):
        self._action("start ActivityIndicator")
        self._running = True

    def stop(self):
        self._action("stop ActivityIndicator")
        self._running = False
