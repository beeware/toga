from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .base import Widget


def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)
    return _handler


class Button(Widget):
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()
        self.label = label
        self.on_press = on_press
        # Buttons have a fixed drawn height. If their space allocation is
        # greater than what is provided, center the button vertically.
        self._expand_vertical = False

    def _startup(self):
        self._impl = Gtk.Button(label=self.label)
        self._impl.connect("clicked", wrapped_handler(self, self.on_press))
