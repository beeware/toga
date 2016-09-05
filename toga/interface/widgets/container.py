from .base import Widget


class Container(Widget):
    def __init__(self, id=None, style=None, children=None):
        super().__init__(id=id, style=style)
        self._children = []
