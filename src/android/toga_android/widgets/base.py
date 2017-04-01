
def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)
    return _handler


class WidgetMixin:
    def _set_app(self, app):
        self._create()

    def _set_window(self, window):
        pass

    def _set_container(self, container):
        if self._impl:
            self._container._impl.addView(self._impl)

    def _add_child(self, child):
        if self._container:
            child._set_container(self._container)

    def _apply_layout(self):
        pass
