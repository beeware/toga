
def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)
    return _handler


class WidgetMixin:
    def _set_app(self, app):
        pass

    def _set_window(self, window):
        pass

    def _set_container(self, container):
        if self._impl:
            self._container._impl.add(self._impl)

    def _add_child(self, child):
        if self._container:
            child._set_container(self._container)
        self.rehint()

    def _apply_layout(self):
        pass

    def rehint(self):
        if self._impl:
            # print("REHINT", self, self._impl.get_preferred_width(), self._impl.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
            hints = {}
            width = self._impl.get_preferred_width()
            height = self._impl.get_preferred_height()

            if width.minimum_width > 0:
                hints['min_width'] = width.minimum_width
            if width.natural_width > 0 and getattr(self, '_fixed_width', False):
                hints['width'] = width.natural_width

            if height.minimum_height > 0:
                hints['min_height'] = height.minimum_height
            if height.natural_height > 0 and getattr(self, '_fixed_height', False):
                hints['height'] = height.natural_height

            if hints:
                self.style.hint(**hints)
