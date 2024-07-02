import asyncio
import sys
from pathlib import Path

from toga.app import overridden
from toga.command import Command, Group
from toga.handlers import simple_handler

from .screens import Screen as ScreenImpl
from .utils import LoggedObject


class App(LoggedObject):
    # Dummy apps close on the last window close
    CLOSE_ON_LAST_WINDOW = True
    # Dummy backend uses default command line handling
    HANDLES_COMMAND_LINE = False

    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        self.dialog_responses = {}

        self.loop = asyncio.get_event_loop()
        self.create()

    def create(self):
        self._action("create App")
        self.interface._startup()

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_app_commands(self):
        self._action("create App commands")
        self.interface.commands.add(
            # Invoke `_request_exit` rather than `exit`, because we want to trigger the
            # "OK to exit?" logic.
            Command(
                simple_handler(self.interface._request_exit),
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

        # If the user has overridden preferences, provide a menu item.
        if overridden(self.interface.preferences):
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.preferences),
                    "Preferences",
                    group=Group.APP,
                    id=Command.PREFERENCES,
                ),
            )

        # If the app has document types, or has overridden new(), provide a menu item.
        if self.interface.document_types:
            known_document_classes = set()
            for extension, document_class in self.interface.document_types.items():
                if document_class not in known_document_classes:
                    self.interface.commands.add(
                        Command(
                            simple_handler(self.interface.new, document_class),
                            text=f"New {document_class.document_type}",
                            group=Group.FILE,
                            id=Command.NEW.format(extension),
                        ),
                    )
                    known_document_classes.add(document_class)
        elif overridden(self.interface.new):
            # If the user has overridden `new`, provide a menu item
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.new),
                    text="New",
                    group=Group.FILE,
                    id=Command.NEW.format(None),
                )
            )

        # If the app has document types, or has overridden open(), provide a menu item.
        if self.interface.document_types or overridden(self.interface.open):
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface._open),
                    text="Open",
                    group=Group.FILE,
                    id=Command.OPEN,
                )
            )

        # If the app has document types, or has overridden save(), provide a menu item.
        if self.interface.document_types or overridden(self.interface.save):
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.save),
                    text="Save",
                    group=Group.FILE,
                    id=Command.SAVE,
                )
            )

        # If the app has document types, or has overridden save_as(), provide a menu item.
        if self.interface.document_types or overridden(self.interface.save_as):
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.save_as),
                    text="Save As",
                    group=Group.FILE,
                    id=Command.SAVE_AS,
                )
            )

        # If the app has document types, or has overridden save_all(), provide a menu
        # item.
        if self.interface.document_types or overridden(self.interface.save_all):
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.save_all),
                    text="Save All",
                    group=Group.FILE,
                    id=Command.SAVE_ALL,
                )
            )

    def create_menus(self):
        self._action("create App menus")
        self.n_menu_items = len(self.interface.commands)

        # Replicate the behavior of platforms that have window-level menu handling.
        for window in self.interface.app.windows:
            if hasattr(window._impl, "create_menus"):
                window._impl.create_menus()

    ######################################################################
    # App lifecycle
    ######################################################################

    def exit(self):
        self._action("exit")

    def main_loop(self):
        print("Starting app using Dummy backend.")
        self._action("main loop")

    def set_main_window(self, window):
        # If the window has been tagged as an invalid main window, raise an error.
        if hasattr(window, "_invalid_main_window"):
            raise ValueError("Invalid dummy main window value")

        self._action("set_main_window", window=window)

    ######################################################################
    # App resources
    ######################################################################

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

    def set_icon(self, icon):
        self._action("set_icon", icon=icon)

    ######################################################################
    # App capabilities
    ######################################################################

    def beep(self):
        self._action("beep")

    def show_about_dialog(self):
        self._action("show_about_dialog")

    ######################################################################
    # Cursor control
    ######################################################################

    def hide_cursor(self):
        self._action("hide_cursor")

    def show_cursor(self):
        self._action("show_cursor")

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        try:
            main_window = self.interface.main_window._impl
        except AttributeError:
            main_window = None

        return self._get_value("current_window", main_window)

    def set_current_window(self, window):
        self._action("set_current_window", window=window)
        self._set_value("current_window", window._impl)

    ######################################################################
    # Full screen control
    ######################################################################

    def enter_full_screen(self, windows):
        self._action("enter_full_screen", windows=windows)

    def exit_full_screen(self, windows):
        self._action("exit_full_screen", windows=windows)

    ######################################################################
    # Simulation interface
    ######################################################################

    def simulate_exit(self):
        self.interface._request_exit()


class DocumentApp(App):
    def create(self):
        self._action("create DocumentApp")

        try:
            # Create and show the document instance
            self.interface._open(Path(sys.argv[1]))
        except IndexError:
            pass

        self.interface._startup()
