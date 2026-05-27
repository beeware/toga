from .container import Container
from .utils import LoggedObject


class Scaffold(LoggedObject):
    def __init__(self, interface):
        self.interface = interface
        self.container = Container()

    def set_content(self, widget):
        self.container.content = widget
        self._action("set content", widget=widget)
        self._set_value("content", widget)

    def refresh(self):
        self._action("refresh")
        if self.content:
            self.content.interface.refresh()

    @property
    def content(self):
        return self.interface.content._impl if self.interface.content else None
