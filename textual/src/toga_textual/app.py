import asyncio

import toga
from textual.app import App as TextualApp

from .screens import Screen as ScreenImpl


class TogaApp(TextualApp):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def on_mount(self) -> None:
        self.impl.create()


class App:
    # Textual apps exit when the last window is closed
    CLOSE_ON_LAST_WINDOW = True
    # Textual apps use default command line handling
    HANDLES_COMMAND_LINE = False

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.loop = asyncio.new_event_loop()
        self.native = TogaApp(self)

        self._current_window = None

        # run the app without displaying it
        self.headless = False

    def create(self):
        self.interface._startup()
        self.set_current_window(self.interface.main_window._impl)

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_standard_commands(self):
        pass

    def create_menus(self):
        self.interface.factory.not_implemented("App.create_menus()")

    ######################################################################
    # App lifecycle
    ######################################################################

    def exit(self):
        self.native.exit()

    def main_loop(self):
        self.loop.run_until_complete(self.native.run_async(headless=self.headless))

    def set_icon(self, icon):
        pass

    def set_main_window(self, window):
        if window is None:
            raise RuntimeError("Session-based apps are not supported on Textual")
        elif window == toga.App.BACKGROUND:
            raise RuntimeError("Background apps are not supported on Textual")
        else:
            self.native.push_screen(self.interface.main_window.id)

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        return [ScreenImpl(window._impl.native) for window in self.interface.windows]

    ######################################################################
    # App state
    ######################################################################

    def get_dark_mode_state(self):
        self.interface.factory.not_implemented("dark mode state")
        return None

    ######################################################################
    # App capabilities
    ######################################################################

    def beep(self):
        self.native.bell()

    def show_about_dialog(self):
        pass

    ######################################################################
    # Cursor control
    ######################################################################

    def show_cursor(self):
        pass

    def hide_cursor(self):
        pass

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        return self._current_window

    def set_current_window(self, window):
        previous_current_window = self._current_window
        self._current_window = window
        self.native.switch_screen(window.native)
        self.native.title = window.get_title()
        if previous_current_window != window:
            if previous_current_window is not None:
                previous_current_window.interface.on_lose_focus()
                previous_current_window.interface.on_hide()
            window.interface.on_gain_focus()
            window.interface.on_show()

    ######################################################################
    # Presentation mode controls
    ######################################################################

    def enter_presentation_mode(self, screen_window_dict):
        self.interface.factory.not_implemented("App.enter_presentation_mode()")

    def exit_presentation_mode(self):
        self.interface.factory.not_implemented("App.exit_presentation_mode()")
