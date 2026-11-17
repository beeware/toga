from toga_dummy.container import Container
from toga_dummy.utils import LoggedObject


class Scaffold(LoggedObject):
    def __init__(self, interface):
        self.interface = interface
        self.container = Container()

    @property
    def window_root(self):
        return self.container

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

    def show_toolbar(self):
        self._action("show toolbar")

    def hide_toolbar(self):
        self._action("hide toolbar")

    def create_toolbar(self):
        self._action("create toolbar")

    def clear_toolbar(self):
        self._action("clear toolbar")
