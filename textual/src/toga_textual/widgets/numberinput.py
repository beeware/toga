from decimal import Decimal, InvalidOperation

from textual._context import NoActiveAppError
from textual.widgets import Input as TextualInput
from travertino.size import at_least

from toga.widgets.numberinput import _clean_decimal, _clean_decimal_str

from .base import Widget


class TogaNumberInput(TextualInput):
    def __init__(self, impl):
        super().__init__(type="number")
        self.interface = impl.interface
        self.impl = impl

    def on_focus(self, event: TextualInput.Changed) -> None:
        if on_gain_focus := getattr(self.interface, "on_gain_focus", None):
            on_gain_focus()

    def on_blur(self, event: TextualInput.Changed) -> None:
        self.impl.normalize_display_value()
        if on_lose_focus := getattr(self.interface, "on_lose_focus", None):
            on_lose_focus()

    def on_input_changed(self, event: TextualInput.Changed) -> None:
        if self.impl._programmatic_change:
            self.impl._programmatic_change = False
        else:
            self.impl.on_input_changed()


class NumberInput(Widget):
    def create(self):
        self._step = Decimal(1)
        self._programmatic_change = False
        self.native = TogaNumberInput(self)

    def _set_display_value(self, value):
        old_value = self.native.value
        self._programmatic_change = True
        try:
            self.native.value = "" if value is None else str(value)
        except NoActiveAppError:
            # Textual updates the reactive value before notifying the active app.
            # NumberInput can be initialized before there is an active app context.
            pass
        finally:
            if self.native.value == old_value:
                self._programmatic_change = False

    def on_input_changed(self):
        value = self.native.value
        clean_value = _clean_decimal_str(value)
        if clean_value != value:
            self._set_display_value(clean_value)
            return

        self.interface.on_change()

    def normalize_display_value(self):
        self._set_display_value(self.interface.value)

    def get_readonly(self):
        return self.native.disabled

    def set_readonly(self, value):
        self.native.disabled = value

    def set_step(self, step):
        self._step = step

    def set_min_value(self, value):
        pass

    def set_max_value(self, value):
        pass

    def get_value(self):
        try:
            return _clean_decimal(self.native.value, self._step)
        except InvalidOperation:
            return None

    def set_value(self, value):
        self._set_display_value(value)
        self.interface.on_change()

    @property
    def width_adjustment(self):
        return 2

    @property
    def height_adjustment(self):
        return 2

    def rehint(self):
        self.interface.intrinsic.width = at_least(len(self.native.value) + 4)
        self.interface.intrinsic.height = 3
