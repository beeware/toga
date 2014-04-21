from gi.repository import Gtk

from tailor.gtk.widgets.base import Widget


def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)
    return _handler


class Button(Widget):
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()

        self.on_press = on_press

        self._impl = Gtk.Button(label=label)
        self._impl.connect("clicked", wrapped_handler(self, self.on_press))
