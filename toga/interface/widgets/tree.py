from .base import Widget


class Tree(Widget):
    def __init__(self, headings, id=None, style=None):
        super().__init__(id=id, style=style)
        self.headings = headings

    def _configure(self):
        pass
