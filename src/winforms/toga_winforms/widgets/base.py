from toga_winforms.libs import *


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._container = None
        self.constraints = None
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
            self._container.native.Controls.Add(self.native)

        for child in self.interface.children:
            child._impl.container = container

        self.interface.rehint()

    @property
    def enabled(self):
        return self.native.get_sensitive()

    @enabled.setter
    def enabled(self, value):
        self.native.set_sensitive(value)

    ### APPLICATOR

    def set_bounds(self, x, y, width, height):
        raise NotImplementedException()

    def set_hidden(self, hidden):
        raise NotImplementedException()

    def set_font(self, font):
        raise NotImplementedException()

    def set_background_color(self, color):
        raise NotImplementedException()

    ### INTERFACE

    def add_child(self, child):
        if self.container:
            child._set_container(self.container)

    def rehint(self):
        raise NotImplementedException()

    def set_font(self, font):
        raise NotImplementedException()
