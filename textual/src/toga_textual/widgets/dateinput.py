from datetime import date, timedelta

from textual._context import NoActiveAppError
from textual.widgets import Input as TextualInput
from travertino.size import at_least

from .base import Widget


class TogaDateInput(TextualInput):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface

    def on_focus(self, event: TextualInput.Changed) -> None:
        self.interface.on_gain_focus()

    def on_blur(self, event: TextualInput.Changed) -> None:
        self.interface.on_lose_focus()


class DateInput(Widget):
    def create(self):
        self.native = TogaDateInput(self)
        self._value = date.today()
        self._min = date(1800, 1, 1)
        self._max = date(8999, 12, 31)

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

    def get_min_date(self):
        return self._min

    def set_min_date(self, value):
        self._min = value

    def get_max_date(self):
        return self._max

    def set_max_date(self, value):
        self._max = value

    def change_by_delta(self, delta):
        value = min(max(self._value + timedelta(days=delta), self._min), self._max)
        if value != self._value:
            self.set_value(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.scale_in_horizontal(self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = 3
