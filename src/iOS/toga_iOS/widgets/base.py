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
    def container(self, container):
        self._container = container
        if self.constraints and self.native:
            self._container.native.addSubview_(self.native)
            self.constraints.container = container

        for child in self.interface.children:
            child._impl.container = container
        self.interface.rehint()

    @property
    def enabled(self):
        value = self.native.isEnabled()
        if value == 0:
            return False
        elif value == 1:
            return True
        else:
            raise RuntimeError('Got not allowed return value: {}'.format(value))

    @enabled.setter
    def enabled(self, value):
        self.native.enabled = value

    def add_child(self, child):
        if self.container:
            child.container = self.container

    def add_constraints(self):
        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.constraints = Constraints(self)

    def apply_layout(self):
        if self.constraints:
            self.constraints.update()

    def apply_sub_layout(self):
        pass

    def set_font(self, font):
        self.native.setFont_(font.native)

    def set_enabled(self, value):
        self.native.enabled = value

    def rehint(self):
        pass
