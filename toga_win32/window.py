from __future__ import print_function, absolute_import, division

from .libs import *

import ctypes


class Window(object):
    def __init__(self, position=(100, 100), size=(640, 480)):
        self._app = None
        self._allocated = 0
        self._widgets = {}
        self.position = position
        self.size = size
        self._content = None

        self.startup()

    def startup(self):
        module = kernel32.GetModuleHandleW(None)
        brush = user32.GetSysColorBrush(COLOR_WINDOW)
        self._window_class = WNDCLASS()
        self._window_class.lpszClassName = u'GenericAppClass%d' % id(self)
        self._window_class.lpfnWndProc = WNDPROC(self._wnd_proc)
        self._window_class.style = CS_VREDRAW | CS_HREDRAW
        self._window_class.hInstance = 0
        self._window_class.hIcon = user32.LoadIconW(module, MAKEINTRESOURCE(1))
        self._window_class.hbrBackground = brush
        self._window_class.lpszMenuName = None
        self._window_class.cbClsExtra = 0
        self._window_class.cbWndExtra = 0
        user32.RegisterClassW(byref(self._window_class))

        self._impl = user32.CreateWindowExW(
            0,
            self._window_class.lpszClassName,
            u'',
            WS_OVERLAPPEDWINDOW,
            self.position[0],
            self.position[1], # CW_USEDEFAULT,
            self.size[0],
            self.size[1],
            0,
            0,
            self._window_class.hInstance,
            0)

        print(1,self._impl)
        # user32.SetWindowPos(self._impl, HWND_NOTOPMOST,
                # position[0], position[1], size[0], size[1], SWP_NOMOVE | SWP_FRAMECHANGED)

        ctypes.windll.UxTheme.SetWindowTheme(self._impl, c_wchar_p('Explorer'), 0)

        user32.SetWindowTextW(self._impl, c_wchar_p("Hello World"))
        print(2, self._impl)

        if self.content:
            self.content.app = self.app

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.app = self.app
        self._content.window = self

    def show(self):
        print(3,self._impl)
        user32.ShowWindow(self._impl, SW_SHOWDEFAULT)
        print(4,self._impl)

    def _allocate_id(self):
        self._allocated = self._allocated + 1
        return self._allocated

    def _wnd_proc(self, hwnd, msg, wParam, lParam):
        try:
            result = {
                WM_CLOSE: self._wm_close,
                WM_COMMAND: self._wm_command,
                WM_SIZE: self._wm_size,
                WM_GETMINMAXINFO: self._wm_getminmaxinfo,
            }[msg](msg, wParam, lParam)
        except KeyError:
            # print "no handler for", msg
            result = 0

        if not result and msg != WM_CLOSE:
            result = user32.DefWindowProcW(hwnd, msg, wParam, lParam)

        return result

    def _wm_command(self, msg, wParam, lParam):
        print("COMMAND RECEIVED", wParam)
        try:
            widget = self._widgets[wParam]
            if widget.on_press:
                widget.on_press(widget)
        except KeyError:
            pass

        return 0

    def _wm_size(self, msg, wParam, lParam):
        print("RESIZE")
        width = LOWORD(lParam)
        height = HIWORD(lParam)
        print("REQUESTED SIZE", width, height)
        if self._content:
            self._content._resize(width, height)
        return 0

    def _wm_close(self, msg, wParam, lParam):
        self.on_close()
        return 0

    def _wm_getminmaxinfo(self, msg, wParam, lParam):
        print("REQUEST FOR MIN MAX INFO")
        info = MINMAXINFO.from_address(lParam)
        if self._content:
            min_width, preferred_width = self.content._width_hint
            min_height, preferred_height = self.content._height_hint
            print("SET MIN to %sx%s" % (min_width, min_height))
            info.ptMinTrackSize.x = int(min_width)
            info.ptMinTrackSize.y = int(min_height)

        # if self._minimum_size:
        #     info.ptMinTrackSize.x, info.ptMinTrackSize.y = self._client_to_window_size(*self._minimum_size)
        # if self._maximum_size:
        #     info.ptMaxTrackSize.x, info.ptMaxTrackSize.y = self._client_to_window_size(*self._maximum_size)

        return 0

    def on_close(self):
        pass
