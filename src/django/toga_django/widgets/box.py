from .base import Widget
from .. import impl


class Box(Widget):
    def create(self):
        self._impl = impl.Box(
            id=self.id,
            style=self.style,
        )

    def add_child(self, child):
        self._impl.add_child(child._impl)
