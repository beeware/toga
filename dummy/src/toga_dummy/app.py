from .utils import LoggedObject, not_required, not_required_on
from .window import Window


class MainWindow(Window):
    @not_required
    def toga_on_close(self):
        self.action("handle MainWindow on_close")


@not_required
class EventLoop:
    def __init__(self, app):
        self.app = app

    def call_soon_threadsafe(self, handler, *args):
        self.app._action("loop:call_soon_threadsafe", handler=handler, args=args)


class App(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.loop = EventLoop(self)

    def create(self):
        self._action("create")

    @not_required_on("mobile")
    def create_menus(self):
        self._action("create menus")

    def main_loop(self):
        self._action("main loop")

    def set_main_window(self, window):
        self._set_value("main_window", window)

    def show_about_dialog(self):
        self._action("show_about_dialog")

    def exit(self):
        self._action("exit")

    @not_required_on("mobile")
    def current_window(self):
        self._action("current_window")

    @not_required_on("mobile")
    def enter_full_screen(self, windows):
        self._action("enter_full_screen", windows=windows)

    @not_required_on("mobile")
    def exit_full_screen(self, windows):
        self._action("exit_full_screen", windows=windows)

    @not_required_on("mobile")
    def get_cursor_position(self):
        self._get_value("cursor_position")

    @not_required_on("mobile")
    def set_cursor_position(self, value):
        self._action("cursor_position", value=value)
        self._set_value("cursor_position", value)

    @not_required_on("mobile")
    def get_cursor_visibility(self):
        self._get_value("cursor_visible")

    @not_required_on("mobile")
    def set_cursor_visibility(self, value):
        self._action("cursor_visible", value=value)
        self._set_value("cursor_visible", value)

    @not_required_on("mobile")
    def show_cursor(self):
        self._action("show_cursor")

    @not_required_on("mobile")
    def hide_cursor(self):
        self._action("hide_cursor")


@not_required_on("mobile", "web")
class DocumentApp(App):
    pass
