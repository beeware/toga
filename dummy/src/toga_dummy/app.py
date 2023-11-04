import asyncio
import sys
from pathlib import Path

from .utils import LoggedObject
from .window import Window


class MainWindow(Window):
    pass


class App(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self

        self.loop = asyncio.get_event_loop()
        self.create()

    def create(self):
        self._action("create App")
        self.interface._startup()

    def create_menus(self):
        self._action("create App menus")

    def main_loop(self):
        print("Starting app using Dummy backend.")
        self._action("main loop")

    def set_main_window(self, window):
        self._action("set_main_window", window=window)

    def show_about_dialog(self):
        self._action("show_about_dialog")

    def beep(self):
        self._action("beep")

    def exit(self):
        self._action("exit")

    def get_current_window(self):
        try:
            return self._get_value("current_window", self.interface.main_window._impl)
        except AttributeError:
            return None

    def set_current_window(self, window):
        self._action("set_current_window", window=window)
        self._set_value("current_window", window._impl)

    def enter_full_screen(self, windows):
        self._action("enter_full_screen", windows=windows)

    def exit_full_screen(self, windows):
        self._action("exit_full_screen", windows=windows)

    def show_cursor(self):
        self._action("show_cursor")

    def hide_cursor(self):
        self._action("hide_cursor")

    def simulate_exit(self):
        self.interface.on_exit()


class DocumentApp(App):
    def create(self):
        self._action("create DocumentApp")
        self.interface._startup()

        try:
            # Create and show the document instance
            self.interface._open(Path(sys.argv[1]))
        except IndexError:
            pass
