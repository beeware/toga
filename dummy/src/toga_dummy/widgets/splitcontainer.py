from toga.constants import Direction

from ..window import Container
from .base import Widget


class SplitContainer(Widget):
    def create(self):
        self._action("create SplitContainer")
        self._content = []

    def set_content(self, content, flex):
        self._action("set content", content=content, flex=flex)
        for widget in content:
            self._content.append(Container(widget))

    def get_direction(self):
        return self._get_value("direction", Direction.VERTICAL)

    def set_direction(self, value):
        self._set_value("direction", value)
