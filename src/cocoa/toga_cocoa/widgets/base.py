from ..container import Constraints


class Widget:
    def __init__(self, interface):
        self._interface = interface
        self._interface._impl = self
        self.create()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    def set_container(self, container):
        if self._constraints and self._native:
            self._interface._container._native.addSubview_(self._native)
            self._constraints._container = container
        self._interface.rehint()

    def add_child(self, child):
        if self._interface._container:
            child._set_container(self._container)

    def add_constraints(self):
        self._native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._constraints = Constraints(self)

    def apply_layout(self):
        if self._constraints:
            self._constraints.update()

    def set_font(self, font):
        self._native.setFont_(font._native)

    def set_enabled(self, value):
        self._native.setEnabled_(value)

    def rehint(self):
        pass