from __future__ import print_function, absolute_import, division

from ..libs import *

from .base import Widget

def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)
    return _handler


class Button(Widget):
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()
        self._expand_vertical = False
        self.label = label
        self.on_press = on_press

    def startup(self):
        x, y, width, height = self._geometry
        print("CREATE AT ", x, y, width, height)
        identifier = self.window._allocate_id()
        self._impl = user32.CreateWindowExW(0, c_wchar_p("button"), c_wchar_p(self.label),
                  WS_CHILD | WS_VISIBLE | BS_DEFPUSHBUTTON | BS_TEXT,
                  int(x), int(y), int(width), int(height),
                  self.window._impl, identifier, 0, 0)

        print("CREATE BUTTON", identifier, self.label)
        self.window._widgets[identifier] = self

    def _resize(self):
        x, y, width, height = self._geometry
        print("RESIZE", self.label,x,y,width,height)
        user32.SetWindowPos(self._impl, HWND_TOP,
                  int(x), int(y), int(width), int(height),
                  0)

    @property
    def _width_hint(self):
        return 130, 130

    @property
    def _height_hint(self):
        return 30, 30

    @property
    def _geometry(self):
        min_width, preferred_width = self._width_hint
        min_height, preferred_height = self._height_hint

        x_pos = self._bounding_box.x.value
        if self._expand_horizontal:
            width = self._bounding_box.width.value
        else:
            x_pos = x_pos + ((self._bounding_box.width.value - preferred_width) / 2.0)
            width = preferred_width

        y_pos = self._bounding_box.y.value
        if self._expand_vertical:
            height = self._bounding_box.height.value
        else:
            y_pos = y_pos + ((self._bounding_box.height.value - preferred_height) / 2.0)
            height = preferred_height

        return (x_pos, y_pos, width, height)
