from textual._context import NoActiveAppError
from textual.widgets import Input as TextualInput
from travertino.size import at_least

from .base import Widget


class TogaInput(TextualInput):
    def __init__(self, impl, **kwargs):
        super().__init__(**kwargs)
        self.interface = impl.interface
        self.impl = impl

    def on_focus(self, event: TextualInput.Changed) -> None:
        self.interface.on_gain_focus()

    def on_blur(self, event: TextualInput.Changed) -> None:
        self.interface.on_lose_focus()

    def on_input_changed(self, event: TextualInput.Changed) -> None:
        if self.impl._programmatic_change:
            self.impl._programmatic_change = False
        else:
            self.interface._value_changed()

    def on_input_submitted(self, event: TextualInput.Submitted) -> None:
        self.interface.on_confirm()


class TextInput(Widget):
    def create(self):
        self._is_valid = True
        self._programmatic_change = False
        self.native = TogaInput(self)

    def get_readonly(self):
        return self.native.disabled

    def set_readonly(self, value):
        self.native.disabled = value

    def get_placeholder(self):
        return self.native.placeholder

    def set_placeholder(self, value):
        self.native.placeholder = value

    def get_value(self):
        return self.native.value

    def set_value(self, value):
        old_value = self.native.value
        self._programmatic_change = True
        try:
            self.native.value = value
        except NoActiveAppError:
            # Textual updates the reactive value before trying to notify the active
            # app. Toga can set values before the widget is mounted, when there is no
            # active Textual app context yet.
            pass
        finally:
            if self.native.value == old_value:
                self._programmatic_change = False

        if self.native.value != old_value:
            self.interface._value_changed()

    def set_error(self, error_message):
        self._is_valid = False

    def clear_error(self):
        self._is_valid = True

    def is_valid(self):
        return self._is_valid

    @property
    def width_adjustment(self):
        return 2

    @property
    def height_adjustment(self):
        return 2

    def rehint(self):
        self.interface.intrinsic.width = at_least(len(self.native.value) + 4)
        self.interface.intrinsic.height = 3
