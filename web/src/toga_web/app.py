import asyncio

import toga
from toga_web.libs import create_element, js

from .screens import Screen as ScreenImpl


class App:
    # Web apps exit when the last window is closed
    CLOSE_ON_LAST_WINDOW = True
    # Web apps use default command line handling
    HANDLES_COMMAND_LINE = False

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.loop = asyncio.new_event_loop()

    def create(self):
        self.native = js.document.getElementById("app-placeholder")
        # self.resource_path = ???

        # Call user code to populate the main window
        self.interface._startup()

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_standard_commands(self):
        pass

    def create_menus(self):
        # Web menus are created on the Window.
        for window in self.interface.windows:
            # It's difficult to trigger this on a simple window, because we can't easily
            # modify the set of app-level commands that are registered, and a simple
            # window doesn't exist when the app starts up. Therefore, no-branch the else
            # case.
            if hasattr(window._impl, "create_menus"):  # pragma: no branch
                window._impl.create_menus()

    ######################################################################
    # App lifecycle
    ######################################################################

    def exit(self):
        pass

    def main_loop(self):
        self.create()

    def set_icon(self, icon):
        pass

    def set_main_window(self, window):
        if window is None:
            raise RuntimeError("Session-based apps are not supported on Web")
        elif window == toga.App.BACKGROUND:
            raise RuntimeError("Background apps are not supported on Web")

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        return [ScreenImpl(js.document.documentElement)]

    ######################################################################
    # App capabilities
    ######################################################################

    def beep(self):
        self.interface.factory.not_implemented("App.beep()")

    def show_about_dialog(self):
        name_and_version = f"{self.interface.formal_name}"

        if self.interface.version is not None:
            name_and_version += f" v{self.interface.version}"

        if self.interface.author is not None:
            copyright = f"\n\nCopyright © {self.interface.author}"

        close_button = create_element(
            "sl-button", slot="footer", variant="primary", content="Ok"
        )
        about_dialog = create_element(
            "sl-dialog",
            id="toga-about-dialog",
            label="About",
            children=[
                create_element("p", content=name_and_version),
                create_element("p", content=copyright),
                close_button,
            ],
        )

        # Create a button handler to capture the close,
        # and destroy the dialog
        def dialog_close(event):
            about_dialog.hide()
            self.native.removeChild(about_dialog)

        close_button.onclick = dialog_close

        # Add the dialog to the DOM.
        self.native.appendChild(about_dialog)

        # If this is the first time a dialog is being shown, the Shoelace
        # autoloader needs to construct the Dialog custom element. We can't
        # display the dialog until that element has been fully loaded and
        # constructed. Only show the dialog when the promise of <sl-dialog>
        # element construction has been fulfilled.
        def show_dialog(promise):
            about_dialog.show()

        js.customElements.whenDefined("sl-dialog").then(show_dialog)

    ######################################################################
    # Cursor control
    ######################################################################

    def show_cursor(self):
        self.interface.factory.not_implemented("App.show_cursor()")

    def hide_cursor(self):
        self.interface.factory.not_implemented("App.hide_cursor()")

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        self.interface.factory.not_implemented("App.get_current_window()")

    def set_current_window(self):
        self.interface.factory.not_implemented("App.set_current_window()")

    ######################################################################
    # Full screen control
    ######################################################################

    def enter_full_screen(self, windows):
        self.interface.factory.not_implemented("App.enter_full_screen()")

    def exit_full_screen(self, windows):
        self.interface.factory.not_implemented("App.exit_full_screen()")
