from .base import Widget


class Switch(Widget):
    def create(self):
        self._action("create Switch")

    def set_text(self, text):
        self._set_value("text", text)

    def set_value(self, value):
        self._set_value("value", value)

    def get_value(self):
        return self._get_value("value")

    def simulate_toggle(self):
        self.interface.on_change(None)
