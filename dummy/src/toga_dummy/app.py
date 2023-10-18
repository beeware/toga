import asyncio

from .utils import LoggedObject, not_required_on
from .window import Window


class MainWindow(Window):
    pass


class App(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.loop = asyncio.new_event_loop()

    def create(self):
        self._action("create")
        self.interface._startup()

    @not_required_on("mobile")
    def create_menus(self):
        self._action("create menus")

    def main_loop(self):
        print("Starting app using Dummy backend.")
        self._action("main loop")
        self.create()

    def set_main_window(self, window):
        self._set_value("main_window", window)

    def show_about_dialog(self):
        self._action("show_about_dialog")

    def beep(self):
        self._action("beep")

    def exit(self):
        self._action("exit")

    @not_required_on("mobile")
    def get_current_window(self):
        self._action("get_current_window")

    @not_required_on("mobile")
    def set_current_window(self):
        self._action("set_current_window")

    @not_required_on("mobile")
    def enter_full_screen(self, windows):
        self._action("enter_full_screen", windows=windows)

    @not_required_on("mobile")
    def exit_full_screen(self, windows):
        self._action("exit_full_screen", windows=windows)

    @not_required_on("mobile")
    def show_cursor(self):
        self._action("show_cursor")

    @not_required_on("mobile")
    def hide_cursor(self):
        self._action("hide_cursor")


@not_required_on("mobile", "web")
class DocumentApp(App):
    pass
