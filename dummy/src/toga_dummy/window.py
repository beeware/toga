import asyncio
from pathlib import Path

import toga_dummy
from toga.constants import WindowState
from toga.types import Size
from toga.window import _initial_position

from .screens import Screen as ScreenImpl
from .utils import LoggedObject


class Window(LoggedObject):
    def __init__(self, interface, title, position, size):
        super().__init__()
        self._action(f"create {self.__class__.__name__}")
        self.interface = interface
        self.dialog_responses = {}
        # Currently, there is not a scaffold.
        self.scaffold = None

        self.set_title(title)
        self.set_position(position if position is not None else _initial_position())

        # We cannot store the following values on the EventLog, since they would be
        # cleared on EventLog.reset(), thereby preventing us from testing no-op
        # condition of requesting the same value as current.
        self._size = size if size else Size(640, 480)
        self._state = WindowState.NORMAL
        self._visible = False

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return self._get_value("title")

    def set_title(self, title):
        self._set_value("title", title)

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):
        self._action("close")
        self._set_value("visible", False)

    def set_app(self, app):
        self._set_value("app", app)

    def show(self):
        self._action("show")
        self._visible = True
        self.interface.on_show()

    ######################################################################
    # Window content and resources
    ######################################################################

    def set_scaffold(self, scaffold):
        self.scaffold = self.interface.scaffold._impl
        self.native_content = scaffold.native_content
        self.manage_scaffold_toolbar()
        self._action("set scaffold", scaffold=scaffold)
        self._set_value("scaffold", scaffold)

    def manage_scaffold_toolbar(self):
        self.scaffold.clear_toolbar()
        self.scaffold.hide_toolbar()

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self) -> Size:
        return self._size

    def set_size(self, size):
        self._action("set size")
        self._size = size
        self.interface.on_resize()

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        # `window.screen` will return `Secondary Screen`
        return ScreenImpl(native=("Secondary Screen", (-1366, -768), (1366, 768)))

    def get_position(self):
        return self._get_value("position")

    def set_position(self, position):
        self._set_value("position", position)

    ######################################################################
    # Window visibility
    ######################################################################

    def get_visible(self):
        return self._visible

    def hide(self):
        self._action("hide")
        self._visible = False
        self.interface.on_hide()

    ######################################################################
    # Window state
    ######################################################################

    def get_window_state(self, in_progress_state=False):
        return self._state

    def set_window_state(self, state):
        previous_state = self._state

        self._action(f"set window state to {state}", state=state)
        self._state = state
        current_state = self._state
        if previous_state != current_state:
            if previous_state == WindowState.MINIMIZED:
                self.interface.on_show()
            elif current_state == WindowState.MINIMIZED:
                self.interface.on_hide()
            # Window is on secondary screen(1366x768), so set the window sizes
            # accordingly.
            match current_state:
                case WindowState.NORMAL:
                    self.set_size(Size(640, 480))
                case WindowState.MAXIMIZED:
                    self.set_size(Size(1366, 728))
                case WindowState.FULLSCREEN:
                    self.set_size(Size(1366, 748))
                case WindowState.PRESENTATION:
                    self.set_size(Size(1366, 768))
                case _:  # WindowState.MINIMIZED
                    pass

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        self._action("get image data")
        path = Path(toga_dummy.__file__).parent / "resources/screenshot.png"
        return path.read_bytes()

    ######################################################################
    # Simulation interface
    ######################################################################

    def simulate_close(self):
        result = self.interface.on_close()
        if isinstance(result, asyncio.Task):
            self.interface.app.loop.run_until_complete(result)


class MainWindow(Window):
    def create_menus(self):
        self._action("create Window menus")

    def create_toolbar(self):
        self.scaffold.create_toolbar()

    def manage_scaffold_toolbar(self):
        self.scaffold.clear_toolbar()
        self.scaffold.show_toolbar()
        self.scaffold.create_toolbar()
