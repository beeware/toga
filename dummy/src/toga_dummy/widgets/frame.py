from ..window import Container
from .base import Widget


class Frame(Widget):
    def create(self):
        self._action("create Frame")
        self.frame_container = Container()

    def set_content(self, widget):
        self.frame_container.content = widget
        self._action("set content", widget=widget)

    def get_title(self):
        return self._get_value("title", "")

    def set_title(self, value):
        self._set_value("title", value)
