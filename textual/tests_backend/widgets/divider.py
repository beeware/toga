from textual.widgets import Rule as TextualRule

from toga.constants import Direction

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = TextualRule

    @property
    def width(self):
        if self.widget.direction == Direction.VERTICAL or self.native.region.width <= 1:
            return 1

        return super().width

    @property
    def height(self):
        if (
            self.widget.direction == Direction.HORIZONTAL
            or self.native.region.height <= 1
        ):
            return 1

        return super().height
