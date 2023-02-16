from .base import Widget


class Button(Widget):
    def create(self):
        self._action("create Button")

    def set_text(self, text):
        self._set_value("text", text)

    def get_text(self):
        return self._get_value("text")

    def set_on_press(self, handler):
        self._set_value("on_press", handler)
