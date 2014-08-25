from __future__ import print_function, absolute_import, division

from toga_cassowary.widget import Widget as CassowaryWidget
from ..libs.constants import *
from ..libs import user32
from ctypes import c_wchar_p

class Widget(CassowaryWidget):
    window_class = None
    default_style = WS_VISIBLE | WS_CHILD
    control_style = 0

    def __init__(self, text=''):
        self.text = text
        super(Widget, self).__init__()


    @property
    def _width_hint(self):
        return (100, 100)

    @property
    def _height_hint(self):
        return (100, 100)

    def create_win32_window(self, window_class=None, text="", style=0, identifier=None, ):
        window_class = window_class or self.window_class
        window_class = c_wchar_p(window_class)
        text = c_wchar_p(text)
        style |= self.default_style
        style |= self.control_style
        x, y, width, height = [int(i) for i in self._geometry]
        parent = self.window._impl
        self._impl = user32.CreateWindowExW(0, window_class, text, style, x, y, width, height, parent, identifier, 0, 0)

    def startup(self):
        identifier = self.window._allocate_id()
        self.create_win32_window(text=self.text, identifier=identifier)
        self.window._widgets[identifier] = self


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

    def _resize(self):
        x, y, width, height = self._geometry
        print("RESIZE", self.text,x,y,width,height)
        user32.SetWindowPos(self._impl, HWND_TOP,
                  int(x), int(y), int(width), int(height),
                  0)


    def _on_wm_command(self, msg, wParam, lParam):
        "Called when a WM_COMMAND message is received referencing this widget."
        pass
