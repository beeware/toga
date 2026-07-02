from textual.widgets import Rule as TextualRule
from travertino.size import at_least

from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = TextualRule()

    def get_direction(self):
        return (
            self.interface.VERTICAL
            if self.native.orientation == "vertical"
            else self.interface.HORIZONTAL
        )

    def set_direction(self, value):
        self.native.orientation = (
            "vertical" if value == self.interface.VERTICAL else "horizontal"
        )

    def rehint(self):
        if self.get_direction() == self.interface.VERTICAL:
            self.interface.intrinsic.width = 1
            self.interface.intrinsic.height = at_least(1)
        else:
            self.interface.intrinsic.width = at_least(1)
            self.interface.intrinsic.height = 1
