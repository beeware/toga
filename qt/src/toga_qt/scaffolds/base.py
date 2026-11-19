from ..container import Container


class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self._title = ""
        self.container = Container(on_refresh=self.content_refreshed)
        self.container.native.resizeEvent = self.qt_container_resize

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

    def qt_container_resize(self, event):
        self.refresh()

    def content_refreshed(self, container):
        min_width = self.interface.content.layout.min_width
        min_height = self.interface.content.layout.min_height
        self.container.native.setMinimumSize(min_width, min_height)
        self.container.min_width = min_width
        self.container.min_height = min_height
