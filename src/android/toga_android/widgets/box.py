from toga.interface import Box as BoxInterface

from .base import WidgetMixin


class Box(BoxInterface, WidgetMixin):
    def __init__(self, id=None, style=None, children=None):
        super().__init__(id=id, style=style, children=children)

    def create(self):
        pass

    def rehint(self):
        # print("REHINT BOX", self.children)
        for child in self.children:
            child.rehint()
