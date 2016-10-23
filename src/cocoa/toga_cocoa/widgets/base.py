from ..container import Constraints


class WidgetMixin:
    def _set_app(self, app):
        pass

    def _set_window(self, window):
        pass

    def _set_container(self, container):
        if self._constraints and self._impl:
            self._container._impl.addSubview_(self._impl)
            self._constraints._container = container
        self.rehint()

    def _add_child(self, child):
        if self._container:
            child._set_container(self._container)

    def _add_constraints(self):
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._constraints = Constraints(self)

    def _apply_layout(self):
        if self._constraints:
            self._constraints.update()

    def rehint(self):
        pass

    def _set_font(self, font):
        self._impl.setFont_(font._impl)
