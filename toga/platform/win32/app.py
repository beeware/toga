import ctypes

from .libs import *
from .window import Window


class MainWindow(Window):
    def on_close(self):
        user32.PostQuitMessage(0)


class App(object):
    def __init__(self, name, app_id):
        self.main_window = MainWindow()

    def main_loop(self):
        self.main_window.show()

        # Main message handling loop.
        msg = MSG()
        while user32.GetMessageW(ctypes.byref(msg), NULL, 0, 0):
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
