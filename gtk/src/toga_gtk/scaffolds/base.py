from ..container import TogaContainer


class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self._title = ""
        self.container = TogaContainer()

    @property
    def current_container(self):
        return self.container

    def set_content(self, widget):
        self.container.content = widget

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def refresh(self):
        if self.container.content:
            self.container.content.interface.refresh()
