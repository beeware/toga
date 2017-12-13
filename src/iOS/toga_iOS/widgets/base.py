from toga_iOS.container import Constraints


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
        if self.constraints and self.native:
            self._container.native.addSubview_(self.native)
            self.constraints.container = container

        for child in self.interface.children:
            child._impl.container = container
        self.interface.rehint()

    def set_enabled(self, value):
        self.native.enabled = value

    ### APPLICATOR

    def set_bounds(self, x, y, width, height):
        raise NotImplementedError()

    def set_hidden(self, hidden):
        raise NotImplementedError()

    def set_font(self, font):
        raise NotImplementedError()

    def set_background_color(self, color):
        raise NotImplementedError()

    ### INTERFACE

    def add_child(self, child):
        if self.container:
            child.container = self.container

    def add_constraints(self):
        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.constraints = Constraints(self)

    def rehint(self):
        pass
