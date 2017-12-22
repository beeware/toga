
class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.native = None
        self.create()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        self._container = container

        if self.native:
            self._container.native.addSubview_(self.native)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        self.native.enabled = value

    ### APPLICATOR

    def set_bounds(self, x, y, width, height):
        # No implementation required here; the new sizing will be picked up
        # by the container layout.
        pass

    def set_hidden(self, hidden):
        pass

    def set_font(self, font):
        pass

    def set_background_color(self, color):
        pass

    ### INTERFACE

    def add_child(self, child):
        if self.container:
            child.viewport = self.root.viewport
            child.container = self.container

    def rehint(self):
        pass
