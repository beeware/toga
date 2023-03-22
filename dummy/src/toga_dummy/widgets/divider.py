from .base import Widget


class Divider(Widget):
    def create(self):
        self._action("create Divider")

    def get_direction(self):
        return self._get_value("direction")

    def set_direction(self, value):
        self._set_value("direction", value)
