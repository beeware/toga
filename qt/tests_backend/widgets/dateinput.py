from PySide6.QtWidgets import QDateEdit

from .base import SimpleProbe


class DateTimeInputProbe(SimpleProbe):
    native_class = QDateEdit
    supports_limits = True


class DateInputProbe(DateTimeInputProbe):
    native_class = QDateEdit

    @property
    def value(self):
        return self.native.date().toPython()

    @property
    def min_value(self):
        return self.native.minimumDate().toPython()

    @property
    def max_value(self):
        return self.native.maximumDate().toPython()

    async def change(self, delta):
        self.native.setDate(self.native.date().addDays(delta))
