from travertino.size import at_least

from textual.containers import Container as TextualContainer
from toga.style.pack import ROW

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = TextualContainer()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        # The layout doesn't have a concept of flow direction; this is a property of the
        # style language. However, we don't have any other way to establish whether this
        # is a row or a column box.
        if self.interface.style.direction == ROW:
            self.native.styles.layout = "horizontal"
        else:
            self.native.styles.layout = "vertical"

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
