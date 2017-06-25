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

    def _set_hidden(self, status, children):
        for view in self._container._impl.subviews:
            [view.setHidden_(status) for c in children if c._impl == view]

    def _hide(self, children):
        if self._container:
            self._set_hidden(True, children)

    def _show(self, children):
        if self._container:
            self._set_hidden(False, children)

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
