from ..container import Container


class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self._title = ""
        self.container = Container(on_refresh=self.content_refreshed)

    @property
    def window(self):
        # The window impl this scaffold is displayed in, if any. The interface
        # window's _impl is None while the window impl is being constructed.
        window = self.interface.window
        return window._impl if window is not None else None

    @property
    def current_container(self):
        return self.container

    def set_content(self, widget):
        self.container.set_content(widget)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def refresh(self):
        if self.container.content:
            self.container.content.interface.refresh()

    def content_refreshed(self, container):
        window = self.window
        if window is not None:
            window.scaffold_refreshed(self)
