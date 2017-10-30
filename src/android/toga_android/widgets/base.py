
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

    def add_child(self, child):
        if self._container:
            child._set_container(self._container)

    def apply_layout(self):
        pass

    def apply_sub_layout(self):
        pass

    def set_font(self, font):
        self.native.setFont_(font.native)

    @property
    def enabled(self):
        raise NotImplementedError()

    @enabled.setter
    def enabled(self, value):
        self.native.enabled = value

    def rehint(self):
        pass
