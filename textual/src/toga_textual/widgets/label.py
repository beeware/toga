from textual.widgets import Label as TextualLabel

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = TextualLabel()

    def get_text(self):
        return self.native.renderable

    def set_text(self, value):
        self.native.renderable = value
