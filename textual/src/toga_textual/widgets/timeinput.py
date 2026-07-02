from datetime import time

from textual._context import NoActiveAppError
from textual.widgets import Input as TextualInput
from travertino.size import at_least

from .base import Widget


class TogaTimeInput(TextualInput):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface

    def on_focus(self, event: TextualInput.Changed) -> None:
        self.interface.on_gain_focus()

    def on_blur(self, event: TextualInput.Changed) -> None:
        self.interface.on_lose_focus()


def seconds_since_midnight(value):
    return value.hour * 3600 + value.minute * 60 + value.second


def time_from_seconds(value):
    return time(value // 3600, (value % 3600) // 60, value % 60)


class TimeInput(Widget):
    def create(self):
        self.native = TogaTimeInput(self)
        self._value = time(0, 0, 0)
        self._min = time(0, 0, 0)
        self._max = time(23, 59, 59)

    def get_value(self):
        return self._value

    def set_value(self, value):
        old_value = self._value
        self._value = value
        try:
            self.native.value = value.isoformat()
        except NoActiveAppError:
            # Values can be set before the widget has been mounted.
            pass

        if value != old_value:
            self.interface.on_change()

    def get_min_time(self):
        return self._min

    def set_min_time(self, value):
        self._min = value

    def get_max_time(self):
        return self._max

    def set_max_time(self, value):
        self._max = value

    def change_by_delta(self, delta):
        value = seconds_since_midnight(self._value) + delta * 60
        value = min(
            max(value, seconds_since_midnight(self._min)),
            seconds_since_midnight(self._max),
        )
        value = time_from_seconds(value)
        if value != self._value:
            self.set_value(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.scale_in_horizontal(self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = 3
