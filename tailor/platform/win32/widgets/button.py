from .base import Widget


class Button(Widget):
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()

    #     self._window_class = WNDCLASS()
    #     self._window_class.lpszClassName = u'GenericAppClass%d' % id(self)
    #     self._window_class.lpfnWndProc = WNDPROC(self._wnd_proc)
    #     self._window_class.style = CS_VREDRAW | CS_HREDRAW
    #     self._window_class.hInstance = 0
    #     self._window_class.hIcon = user32.LoadIconW(module, MAKEINTRESOURCE(1))
    #     self._window_class.hbrBackground = black
    #     self._window_class.lpszMenuName = None
    #     self._window_class.cbClsExtra = 0
    #     self._window_class.cbWndExtra = 0
    #     user32.RegisterClassW(byref(self._window_class))

    #     self._impl = user32.CreateWindowExW(
    #         0,
    #         "BUTTON",
    #         u'OK',
    #         WS_TABSTOP|WS_VISIBLE|WS_CHILD|BS_DEFPUSHBUTTON,
    #         50,
    #         50,
    #         100,
    #         50,
    #         window,
    #         id(self),
    #         kernel32.GetModuleHandle(0),
    #         0)

    # def show(self):
    #     user32.ShowWindow(self._impl, SW_SHOWDEFAULT)

    # def _wnd_proc(self, hwnd, msg, wParam, lParam):
    #     try:
    #         result = {
    #             WM_CLOSE: self._wm_close
    #         }[msg](msg, wParam, lParam)
    #     except KeyError:
    #         # print "no handler for", msg
    #         result = 0

    #     if not result and msg != WM_CLOSE:
    #         result = user32.DefWindowProcW(hwnd, msg, wParam, lParam)

    #     return result

    # def _wm_close(self, msg, wParam, lParam):
    #     self.on_close()
    #     return 0

    # def on_close(self):
    #     pass
