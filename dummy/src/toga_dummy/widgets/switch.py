from .base import Widget


class Switch(Widget):
    def create(self):
        self._action("create Switch")

    def get_text(self):
        return self._get_value("text")

    def set_text(self, text):
        self._set_value("text", text)

    def get_value(self):
        return self._get_value("value")

    def set_value(self, value):
        old_value = self._get_value("value", None)
        self._set_value("value", value)

        if self.interface.on_change and value != old_value:
            self.interface.on_change(self.interface)

    def set_on_change(self, handler):
        self._set_value("on_change", handler)
