from __future__ import print_function, absolute_import, division

from ..libs import *

from .base import Widget

def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)
    return _handler


class Button(Widget):
    window_class = 'button'
    control_style = BS_DEFPUSHBUTTON | BS_TEXT

    def __init__(self, label, on_press=None):
        super(Button, self).__init__(text=label)
        self._expand_vertical = False
        self.on_press = on_press

    @property
    def _width_hint(self):
        return 130, 130

    @property
    def _height_hint(self):
        return 30, 30
