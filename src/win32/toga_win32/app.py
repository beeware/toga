from __future__ import print_function, absolute_import, division

import ctypes

from .libs import *
from .window import Window


class MainWindow(Window):
    def on_close(self):
        user32.PostQuitMessage(0)


class App(object):
    def __init__(self, name, app_id, icon=None, startup=None):
        self.icon = icon
        self._startup_method = startup
        self.last_focus = None

        self._startup()

    def _startup(self):
        self.main_window = MainWindow()
        self.main_window.app = self
        self.main_window.register_message_handler(WM_ACTIVATE, self.on_activate)
        self.main_window.register_message_handler(WM_SETFOCUS, self.on_set_focus)

        self.startup()

        self.main_window.show()

    def startup(self):
        if self._startup_method:
            self.main_window.content = self._startup_method(self)

    def main_loop(self):

        # Main message handling loop.
        msg = MSG()
        while user32.GetMessageW(ctypes.byref(msg), NULL, 0, 0):
            if user32.IsDialogMessage(self.main_window._impl, ctypes.byref(msg)):
                continue
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def on_set_focus(self, msg, old_focus, wParam):
        if self.last_focus:
            user32.SetFocus(self.last_focus)

    def on_activate(self, msg, state, lParam):
        if state == WA_INACTIVE:
            self.last_focus = user32.GetFocus()
