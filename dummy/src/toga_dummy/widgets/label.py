from .base import Widget


class Label(Widget):
    def create(self):
        self._action("create Label")

    def set_alignment(self, value):
        self._set_value("alignment", value)

    def get_text(self):
        return self._get_value("text")

    def set_text(self, value):
        self._set_value("text", value)
