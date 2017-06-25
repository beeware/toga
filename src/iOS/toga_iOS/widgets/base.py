from ..container import Constraints


class Widget:
    def _set_app(self, app):
        pass

    def _set_window(self, window):
        pass

    def _set_container(self, container):
        if self._constraints and self._native:
            self._creator._container._native.addSubview_(self._native)
            self._constraints._container = container
        self.rehint()

    def _add_child(self, child):
        if self._creator._container:
            child._set_container(self._container)

    def _add_constraints(self):
        self._native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._constraints = Constraints(self)

    def _apply_layout(self):
        if self._constraints:
            self._constraints.update()

    def rehint(self):
        pass

    def _set_font(self, font):
        self._native.setFont_(font._native)

    def set_enabled(self, value):
        self._native.enabled = value