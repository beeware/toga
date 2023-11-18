from decimal import InvalidOperation

from android.text import InputType

from toga.widgets.numberinput import _clean_decimal

from .textinput import TextInput


class NumberInput(TextInput):
    def create(self):
        super().create(
            InputType.TYPE_CLASS_NUMBER
            | InputType.TYPE_NUMBER_FLAG_DECIMAL
            | InputType.TYPE_NUMBER_FLAG_SIGNED,
        )

    def get_value(self):
        try:
            return _clean_decimal(super().get_value(), self.interface.step)
        except InvalidOperation:
            return None

    def set_value(self, value):
        super().set_value("" if value is None else str(value))

    def set_step(self, step):
        pass  # This backend doesn't support stepped increments.

    def set_max_value(self, value):
        pass  # This backend doesn't support stepped increments.

    def set_min_value(self, value):
        pass  # This backend doesn't support stepped increments.

    def _on_change(self):
        self.interface.on_change()

    def _on_confirm(self):  # pragma: nocover
        pass  # The interface doesn't support this event.

    def _on_gain_focus(self):
        pass  # The interface doesn't support this event.

    def _on_lose_focus(self):
        # The interface doesn't support this event, but we should still clip the
        # displayed value.
        self.set_value(self.interface.value)
