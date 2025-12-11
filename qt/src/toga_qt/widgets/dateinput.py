from datetime import date

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDateEdit
from travertino.size import at_least

from .base import Widget


class DateInput(Widget):
    def create(self):
        self.native = QDateEdit()
        self.native.setCalendarPopup(True)
        self.native.dateChanged.connect(self.qt_on_change)

    def qt_on_change(self, value):
        self.interface.on_change()

    def get_value(self):
        return self.native.date().toPython()

    def set_value(self, value: date):
        self.native.setDate(self._qdate_from_python(value))

    def get_min_date(self):
        return self.native.minimumDate().toPython()

    def set_min_date(self, value):
        self.native.setMinimumDate(self._qdate_from_python(value))

    def get_max_date(self):
        return self.native.maximumDate().toPython()

    def set_max_date(self, value):
        self.native.setMaximumDate(self._qdate_from_python(value))

    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, size.width())
        )
        self.interface.intrinsic.height = size.height()

    def _qdate_from_python(self, value: date) -> QDate:
        return QDate(value.year, value.month, value.day)
