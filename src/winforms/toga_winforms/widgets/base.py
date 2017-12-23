from toga_winforms.libs import *


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._container = None
        self.native = None
        self.create()
        self.interface.style.reapply()

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
            self._container.native.Controls.Add(self.native)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        raise NotImplementedException()

    ### APPLICATOR

    def set_bounds(self, x, y, width, height):
        if self.native:
            self.native.Size = Size(width, height)
            self.native.Location = Point(x, y)

    def set_alignment(self, alignment):
        pass

    def set_hidden(self, hidden):
        pass

    def set_font(self, font):
        pass

    def set_color(self, color):
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
