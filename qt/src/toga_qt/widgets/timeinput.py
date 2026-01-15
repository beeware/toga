from datetime import time

from PySide6.QtCore import QTime
from PySide6.QtWidgets import QTimeEdit
from travertino.size import at_least

from .base import Widget


class TimeInput(Widget):
    def create(self):
        self.native = QTimeEdit()
        self.native.timeChanged.connect(self.qt_on_change)

    def qt_on_change(self, value):
        self.interface.on_change()

    def get_value(self):
        return self.native.time().toPython()

    def set_value(self, value: time):
        self.native.setTime(self._qtime_from_python(value))

    def get_min_time(self):
        return self.native.minimumTime().toPython()

    def set_min_time(self, value):
        self.native.setMinimumTime(self._qtime_from_python(value))

    def get_max_time(self):
        return self.native.maximumTime().toPython()

    def set_max_time(self, value):
        self.native.setMaximumTime(self._qtime_from_python(value))

    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, size.width())
        )
        self.interface.intrinsic.height = size.height()

    def _qtime_from_python(self, value: time) -> QTime:
        return QTime(
            value.hour,
            value.minute,
            value.second,
            int(round(value.microsecond / 1000)),
        )
