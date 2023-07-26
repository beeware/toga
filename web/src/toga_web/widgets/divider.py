from toga.constants import Direction

from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-divider")

    def get_direction(self):
        return self.interface.direction

    def set_direction(self, value):
        if value is Direction.VERTICAL:
            self.native.setAttribute("vertical", "")
        else:
            self.native.removeAttribute("vertical")
