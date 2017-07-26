from ..container import Constraints


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
    def container(self, widget):
        self._container = widget
        if self.constraints and self.native:
            self._container.native.addSubview_(self.native)
            self.constraints.container = widget

        for child in self.interface.children:
            child._impl.container = widget
        self.interface.rehint()

    def add_child(self, child):
        if self.container:
            child.container = self.container

    def add_constraints(self):
        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.constraints = Constraints(self)

    def apply_layout(self):
        if self.constraints:
            self.constraints.update()

    def set_font(self, font):
        self.native.setFont_(font.native)

    def set_enabled(self, value):
        self.native.enabled = value

    def rehint(self):
        pass
