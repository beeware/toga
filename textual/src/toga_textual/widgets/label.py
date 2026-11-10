from textual.widgets import Label as TextualLabel
from travertino.size import at_least

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = TextualLabel()

    def get_text(self):
        return str(self.native.renderable)

    def set_text(self, value):
        self.native.update(value)

    def rehint(self):
        lines = str(self.native.renderable).split("\n")
        self.interface.intrinsic.width = at_least(max(map(len, lines), default=0))
        self.interface.intrinsic.height = max(len(lines), 1)
