import asyncio

import toga
from toga.app import overridden

from .screens import Screen as ScreenImpl
from .utils import LoggedObject


class App(LoggedObject):
    # Dummy apps close on the last window close
    CLOSE_ON_LAST_WINDOW = True

    def __init__(self, interface):
        super().__init__()
        self.interface = interface

        self.interface._impl = self
        self.loop = asyncio.get_event_loop()

        self._action("create App")
        self.interface._startup()

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_app_commands(self):
        self.about_command = toga.Command(
            self.interface._menu_about,
            "About",
            group=toga.Group.APP,
        )
        self.exit_command = toga.Command(
            self.interface._menu_exit,
            "Exit",
            group=toga.Group.APP,
        )
        self.visit_homepage_command = toga.Command(
            self.interface._menu_visit_homepage,
            "Visit homepage",
            enabled=self.interface.home_page is not None,
            group=toga.Group.HELP,
        )

        self.interface.commands.add(
            self.about_command,
            self.exit_command,
            self.visit_homepage_command,
        )

        # Register the commands for any app with a MainWindow,
        # or any Session-based app (i.e., app with no main window),
        # or any app that explicitly defines `preferences()`
        if (
            isinstance(self.interface.main_window, toga.MainWindow)
            or self.interface.main_window is None
            or overridden(self.interface.preferences)
        ):
            self.preferences_command = toga.Command(
                self.interface._menu_preferences,
                "Preferences",
                group=toga.Group.APP,
                # For now, only enable preferences if the user defines an implementation
                enabled=overridden(self.interface.preferences),
            )
            self.interface.commands.add(self.preferences_command)

        # Add a "New" menu item for each unique registered document type; or, if there's
        # an overridden new method.
        if self.interface.document_types:
            self.new_commands = {}
            for document_class in self.interface.document_types.values():
                if document_class not in self.new_commands:
                    self.new_commands[document_class] = toga.Command(
                        self.interface._menu_new_document(document_class),
                        text=f"New {document_class.document_type}",
                        group=toga.Group.FILE,
                    )
                    self.interface.commands.add(self.new_commands[document_class])
        elif overridden(self.interface.new):
            self.new_commands = {
                None: toga.Command(
                    self.interface._menu_new_document(None),
                    text="New",
                    group=toga.Group.FILE,
                )
            }
            self.interface.commands.add(self.new_commands[None])

        # If there's a user-provided open() implementation, or there are registered
        # document types, add an Open menu item.
        if overridden(self.interface.open) or self.interface.document_types:
            self.open_command = toga.Command(
                self.interface._menu_open_file,
                text="Open",
                group=toga.Group.FILE,
            )
            self.interface.commands.add(self.open_command)

        # If there is a user-provided save() implementation, or there are registered
        # document types, add a Save menu item.
        if overridden(self.interface.save) or self.interface.document_types:
            self.save_command = toga.Command(
                self.interface._menu_save,
                text="Save",
                group=toga.Group.FILE,
            )
            self.interface.commands.add(self.save_command)

        # If there is a user-provided save_as() implementation, or there are registered
        # document types, add a Save As menu item.
        if overridden(self.interface.save_as) or self.interface.document_types:
            self.save_as_command = toga.Command(
                self.interface._menu_save_as,
                text="Save As",
                group=toga.Group.FILE,
            )
            self.interface.commands.add(self.save_as_command)

        # If there is a user-provided save_all() implementation, or there are registered
        # document types, add a Save All menu item.
        if overridden(self.interface.save_all) or self.interface.document_types:
            self.save_all_command = toga.Command(
                self.interface._menu_save_all,
                text="Save All",
                group=toga.Group.FILE,
            )
            self.interface.commands.add(self.save_all_command)

    def create_menus(self):
        self._action("create App menus")

    ######################################################################
    # App lifecycle
    ######################################################################

    def exit(self):
        self._action("exit")

    def finalize(self):
        self._action("finalize creation")

        self.create_app_commands()
        self.create_menus()

        # Process any command line arguments to open documents, etc
        self.interface._create_initial_windows()

    def main_loop(self):
        print("Starting app using Dummy backend.")
        self._action("main loop")

    def set_main_window(self, window):
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
        self.interface.on_exit()
