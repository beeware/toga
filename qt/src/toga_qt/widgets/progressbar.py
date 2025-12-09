from PySide6.QtWidgets import QProgressBar
from travertino.size import at_least

from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = QProgressBar()

        self.native.setMaximum(100)
        self._running = False
        self._indeterminate = False

    def is_running(self):
        return self._running

    def get_value(self):
        if self._indeterminate:
            return None
        return self.native.value() / 100

    def set_value(self, value):
        if not self._indeterminate:
            self.native.setValue(int(float(value) * 100))

    def get_max(self):
        if self._indeterminate:
            return None
        return self.native.maximum() / 100

    def set_max(self, value):
        if value is None:
            self._indeterminate = True
            if self._running:
                self._start_indeterminate()
            else:
                self._stop_indeterminate()
        else:
            if self._indeterminate:
                self._indeterminate = False
                self.native.setValue(0)
            self.native.setRange(0, int(float(value) * 100))

    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, size.width())
        )
        self.interface.intrinsic.height = size.height()

    def start(self):
        self._running = True
        if self._indeterminate:
            self._start_indeterminate()

    def stop(self):
        self._running = False
        if self._indeterminate:
            self._stop_indeterminate()

    def _start_indeterminate(self):
        self.native.setRange(0, 0)

    def _stop_indeterminate(self):
        # fake "stopped" indeterminate bar with a determinate bar
        self.native.setRange(0, 1)
