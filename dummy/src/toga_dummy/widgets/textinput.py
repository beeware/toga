from .base import Widget


class TextInput(Widget):
    def create(self):
        self._action("create TextInput")

    def get_readonly(self):
        return self._get_value("readonly", False)

    def set_readonly(self, value):
        self._set_value("readonly", value)

    def get_placeholder(self):
        return self._get_value("placeholder", "")

    def set_placeholder(self, value):
        self._set_value("placeholder", value)

    def get_value(self):
        return self._get_value("value", "")

    def set_value(self, value):
        self._set_value("value", value)
        self.simulate_change()

    def set_error(self, error_message):
        self._action("set_error", error_message=error_message)
        self._set_value("valid", False)

    def clear_error(self):
        self._action("clear_error")
        self._set_value("valid", True)

    def is_valid(self):
        return self._get_value("valid")

    def simulate_change(self):
        self.interface._value_changed()

    def simulate_confirm(self):
        self.interface.on_confirm()

    def simulate_gain_focus(self):
        self.interface.on_gain_focus()

    def simulate_lose_focus(self):
        self.interface.on_lose_focus()
