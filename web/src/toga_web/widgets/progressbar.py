from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-progress-bar")
        self._is_running = False
        self._value = 0
        self._max = 0

    def is_running(self):
        return self._is_running

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        self.native.value = self.percentage

    def get_max(self):
        return self._max

    def set_max(self, value):
        self._max = value
        if value is None:
            if self._is_running:
                self.native.indeterminate = True
        else:
            self.native.value = self.percentage
            self.native.indeterminate = False

    def start(self):
        self._is_running = True
        if self._max is None:
            self.native.indeterminate = True

    def stop(self):
        self._is_running = False
        self.native.indeterminate = False

    @property
    def percentage(self):
        if self._max is None or self._max == 0:
            return 0

        return self._value / self._max * 100
