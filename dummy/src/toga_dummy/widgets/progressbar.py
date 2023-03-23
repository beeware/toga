from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self._action("create ProgressBar")
        self._is_running = False

    def is_running(self):
        return self._is_running

    def get_value(self):
        if self.get_max() is None:
            return None
        return self._get_value("value")

    def set_value(self, value):
        self._set_value("value", value)

    def get_max(self):
        return self._get_value("max", default=None)

    def set_max(self, value):
        self._set_value("max", value)

    def start(self):
        self._action("start ProgressBar")
        self._is_running = True

    def stop(self):
        self._action("stop ProgressBar")
        self._is_running = False
