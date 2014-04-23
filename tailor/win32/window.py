from tailor.win32.libs import *


class WindowDelegate(object):
    def __init__(self, interface):
        self.interface = interface

        self._event_handlers = {
            WM_CLOSE: self.wm_close
        }

    def _wnd_proc(self, hwnd, msg, wParam, lParam):
        try:
            result = self._event_handlers[msg](msg, wParam, lParam)
        except KeyError:
            # print "no handler for", msg
            result = 0

        if not result and msg != WM_CLOSE:
            result = user32.DefWindowProcW(hwnd, msg, wParam, lParam)

        return result

    def wm_close(self, msg, wParam, lParam):
        self.interface.on_close()
        return 0


class Window(object):
    def __init__(self, position=(100, 100), size=(640, 480)):

        self._delegate = WindowDelegate(self)

        module = kernel32.GetModuleHandleW(None)
        # white = gdi32.GetStockObject(WHITE_BRUSH)
        black = gdi32.GetStockObject(BLACK_BRUSH)
        self._window_class = WNDCLASS()
        self._window_class.lpszClassName = u'GenericAppClass%d' % id(self)
        self._window_class.lpfnWndProc = WNDPROC(self._delegate._wnd_proc)
        self._window_class.style = CS_VREDRAW | CS_HREDRAW
        self._window_class.hInstance = 0
        self._window_class.hIcon = user32.LoadIconW(module, MAKEINTRESOURCE(1))
        self._window_class.hbrBackground = black
        self._window_class.lpszMenuName = None
        self._window_class.cbClsExtra = 0
        self._window_class.cbWndExtra = 0
        user32.RegisterClassW(byref(self._window_class))

        self._impl = user32.CreateWindowExW(
            0,
            self._window_class.lpszClassName,
            u'',
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            size[0],
            size[1],
            0,
            0,
            self._window_class.hInstance,
            0)

        user32.SetWindowPos(self._impl, HWND_NOTOPMOST,
                position[0], position[1], size[0], size[1], SWP_NOMOVE | SWP_FRAMECHANGED)

        user32.SetWindowTextW(self._impl, c_wchar_p("Hello World"))

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget

    def show(self):
        user32.ShowWindow(self._impl, SW_SHOWDEFAULT)

    def on_close(self):
        pass
