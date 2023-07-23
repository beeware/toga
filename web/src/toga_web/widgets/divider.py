"""
A web widget to display a divider.

This is a web implementation of the `toga.Divider` widget.
Details can be found in https://shoelace.style/components/divider
"""
from toga.constants import Direction

from .base import Widget


class Divider(Widget):
    def create(
        self,
    ):
        self.native = self._create_native_widget("sl-divider")

    def get_direction(self):
        return self.interface.direction

    def set_direction(self, value):
        if value is Direction.VERTICAL:
            self.native.setAttribute("vertical", "")
        else:
            self.native.removeAttribute("vertical")
