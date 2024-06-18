import asyncio
import sys
from pathlib import Path

from toga.app import overridden
from toga.command import Command, Group
from toga.handlers import simple_handler

from .screens import Screen as ScreenImpl
from .utils import LoggedObject


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

    def create_app_commands(self):
        self._action("create App commands")
        self.interface.commands.add(
            Command(
                simple_handler(self.interface.preferences),
                "Preferences",
                group=Group.APP,
                # For now, only enable preferences if the user defines an implementation
                enabled=overridden(self.interface.preferences),
                id=Command.PREFERENCES,
            ),
            # Invoke `on_exit` rather than `exit`, because we want to trigger the "OK to
            # exit?" logic. It's already a bound handler, so we can use it directly.
            Command(
                self.interface.on_exit,
                "Exit",
                group=Group.APP,
                section=sys.maxsize,
                id=Command.EXIT,
            ),
            Command(
                simple_handler(self.interface.about),
                f"About {self.interface.formal_name}",
                group=Group.HELP,
                id=Command.ABOUT,
            ),
            Command(
                simple_handler(self.interface.visit_homepage),
                "Visit homepage",
                enabled=self.interface.home_page is not None,
                group=Group.HELP,
                id=Command.VISIT_HOMEPAGE,
            ),
        )

    def create_menus(self):
        self._action("create App menus")
        self.n_menu_items = len(self.interface.commands)

    def main_loop(self):
        print("Starting app using Dummy backend.")
        self._action("main loop")

    def set_icon(self, icon):
        self._action("set_icon", icon=icon)

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

    def get_screens(self):
        # _________________________________________________
        # Display Setup:                                  |
        # ________________________________________________|
        #              |--1366--|                         |
        # (-1366,-768) _________                          |
        #          |  |         |                         |
        #         768 |Secondary|                         |
        #          |  | Screen  |                         |
        #          |  |_________|(0,0)                    |
        #                          _________              |
        #                      |  |         |             |
        #                    1080 | Primary |             |
        #                      |  | Screen  |             |
        #                      |  |_________|(1920,1080)  |
        #                         |---1920--|             |
        # ________________________________________________|
        #  `window.screen` will return `Secondary Screen` |
        #   as window is on secondary screen to better    |
        #   test out the differences between              |
        #   `window.position` & `window.screen_position`. |
        # ________________________________________________|
        return [
            ScreenImpl(native=("Primary Screen", (0, 0), (1920, 1080))),
            ScreenImpl(native=("Secondary Screen", (-1366, -768), (1366, 768))),
        ]


class DocumentApp(App):
    def create(self):
        self._action("create DocumentApp")
        self.interface._startup()

        try:
            # Create and show the document instance
            self.interface._open(Path(sys.argv[1]))
        except IndexError:
            pass
