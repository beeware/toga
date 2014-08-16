from __future__ import print_function, absolute_import, division

from toga_cassowary.widget import Widget as CassowaryWidget


def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)
    return _handler


class Widget(CassowaryWidget):

    @property
    def _width_hint(self):
        return self._impl.get_preferred_width()

    @property
    def _height_hint(self):
        return self._impl.get_preferred_height()
