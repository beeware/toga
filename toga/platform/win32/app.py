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

        self._startup()

    def _startup(self):
        self.main_window = MainWindow()
        self.main_window.app = self

        self.startup()

        self.main_window.show()

    def startup(self):
        if self._startup_method:
            self.main_window.content = self._startup_method(self)

    def main_loop(self):

        # Main message handling loop.
        msg = MSG()
        while user32.GetMessageW(ctypes.byref(msg), NULL, 0, 0):
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
