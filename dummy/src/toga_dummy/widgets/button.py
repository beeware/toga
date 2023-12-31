from .base import Widget


class Button(Widget):
    def create(self):
        self._action("create Button")

    def get_text(self):
        return self._get_value("text")

    def set_text(self, text):
        self._set_value("text", text)

    def get_icon(self):
        return self._get_value("icon")

    def set_icon(self, icon):
        self._set_value("icon", icon)

    def simulate_press(self):
        self.interface.on_press()
