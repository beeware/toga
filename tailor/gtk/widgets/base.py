from tailor.widget import WidgetBase


def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)
    return _handler


class Widget(WidgetBase):

    @property
    def width_hints(self):
        return self._impl.get_preferred_width()

    @property
    def height_hints(self):
        return self._impl.get_preferred_width()
