from PySide6.QtWidgets import QTimeEdit

from .dateinput import DateTimeInputProbe


class TimeInputProbe(DateTimeInputProbe):
    native_class = QTimeEdit
    supports_seconds = True

    @property
    def value(self):
        return self.native.time().toPython()

    @property
    def min_value(self):
        return self.native.minimumTime().toPython()

    @property
    def max_value(self):
        return self.native.maximumTime().toPython()

    async def change(self, delta):
        self.native.setTime(self.native.time().addSecs(60 * delta))
