
from toga.interface import Box as BoxInterface

from .base import WidgetMixin


class Box(BoxInterface, WidgetMixin):
    def __init__(self, id=id, style=None, children=None):
        super().__init__(id=id, style=style, children=children)
        self._create()

    def create(self):
        pass

    def rehint(self):
        pass
