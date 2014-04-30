from toga.platform.win32.libs import *

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

    def _create(self, window, x, y, width, height):
        print "CREATE AT ", x, y, width, height
        identifier = window._allocate_id()
        self._impl = user32.CreateWindowExW(0, c_wchar_p("button"), c_wchar_p(self.label),
                  WS_CHILD | WS_VISIBLE | BS_DEFPUSHBUTTON | BS_TEXT,
                  int(x), int(y), int(width), int(height),
                  window._impl, identifier, 0, 0)

        print "CREATE BUTTON", identifier, self.label
        window._widgets[identifier] = self

    def _resize(self, x, y, width, height):
        print "RESIZE", self.label,x,y,width,height
        user32.SetWindowPos(self._impl, HWND_TOP,
                  int(x), int(y), int(width), int(height),
                  0)

    @property
    def _width_hint(self):
        return 130, 130

    @property
    def _height_hint(self):
        return 30, 30
