from textual.widgets import Label as TextualLabel
from travertino.size import at_least

from toga_textual.widgets.base import Widget


class HelloWorld(Widget):
    def create(self):
        self.native = TextualLabel()
        self.native.update("Hello World!")

    def rehint(self):
        self.interface.intrinsic.width = at_least(len(self.native.renderable))
        self.interface.intrinsic.height = at_least(1)
