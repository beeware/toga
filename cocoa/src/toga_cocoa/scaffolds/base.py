from toga_cocoa.container import ControlledContainer


class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self.container = ControlledContainer(on_refresh=self.content_refreshed)

    @property
    def current_container(self):
        return self.container

    def set_content(self, widget):
        self.container.content = widget

    @property
    def title(self):
        return self.container.controller.title

    @title.setter
    def title(self, value):
        self.container.controller.title = value

    def refresh(self):
        if self.container.content:
            self.container.content.interface.refresh()

    def content_refreshed(self, container):
        # Apply the minimum size.  This will autoresize the window if needed.
        self.container.min_width = self.interface.content.layout.min_width
        self.container.min_height = self.interface.content.layout.min_height
