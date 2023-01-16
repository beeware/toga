from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        self._action("create MultilineTextInput")

    def set_value(self, value):
        self._set_value("value", value)

    def get_value(self):
        return self._get_value("value")

    def set_placeholder(self, value):
        self._set_value("placeholder", value)

    def set_readonly(self, value):
        self._set_value("readonly", value)

    def set_on_change(self, handler):
        self._set_value("on_change", handler)

    def scroll_to_bottom(self):
        self._action("scroll to bottom")

    def scroll_to_top(self):
        self._action("scroll to top")
