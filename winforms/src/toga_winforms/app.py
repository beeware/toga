import asyncio
import re
import sys
import threading
from ctypes import windll

import System.Windows.Forms as WinForms
from System import Environment, Threading
from System.Media import SystemSounds
from System.Net import SecurityProtocolType, ServicePointManager
from System.Windows.Threading import Dispatcher

import toga
from toga import Key
from toga.app import overridden

from .libs.proactor import WinformsProactorEventLoop
from .libs.wrapper import WeakrefCallable
from .screens import Screen as ScreenImpl


def winforms_thread_exception(sender, winforms_exc):  # pragma: no cover
    # The PythonException returned by Winforms doesn't give us
    # easy access to the underlying Python stacktrace; so we
    # reconstruct it from the string message.
    # The Python message is helpfully included in square brackets,
    # as the context for the first line in the .net stack trace.
    # So, look for the closing bracket and the start of the Python.net
    # stack trace. Then, reconstruct the line breaks internal to the
    # remaining string.
    print("Traceback (most recent call last):")
    py_exc = winforms_exc.get_Exception()
    full_stack_trace = py_exc.StackTrace
    regex = re.compile(
        r"^\[(?:'(.*?)', )*(?:'(.*?)')\]   (?:.*?) Python\.Runtime",
        re.DOTALL | re.UNICODE,
    )

    def print_stack_trace(stack_trace_line):  # pragma: no cover
        for level in stack_trace_line.split("', '"):
            for line in level.split("\\n"):
                if line:
                    print(line)

    stacktrace_relevant_lines = regex.findall(full_stack_trace)
    if len(stacktrace_relevant_lines) == 0:
        print_stack_trace(full_stack_trace)
    else:
        for lines in stacktrace_relevant_lines:
            for line in lines:
                print_stack_trace(line)

    print(py_exc.Message)


class App:
    # Winforms apps exit when the last window is closed
    CLOSE_ON_LAST_WINDOW = True

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        # Winforms app exit is tightly bound to the close of the main window. The
        # FormClosing message on the main window triggers the "on_exit" handler (which
        # might abort the exit). However, on success, it will request the app (and thus
        # the Main Window) to close, causing another close event. So - we have a flag
        # that is only ever sent once a request has been made to exit the native app.
        # This flag can be used to shortcut any window-level close handling.
        self._is_exiting = False

        # Winforms cursor visibility is a stack; If you call hide N times, you
        # need to call Show N times to make the cursor re-appear. Store a local
        # boolean to allow us to avoid building a deep stack.
        self._cursor_visible = True

        self.loop = WinformsProactorEventLoop()
        asyncio.set_event_loop(self.loop)

    def create(self):
        # The winforms App impl's create() is deferred so that it can run inside the GUI
        # thread. This means the app isn't created until the main loop is running.
        self.native = WinForms.Application
        self.app_context = WinForms.ApplicationContext()
        self.app_dispatcher = Dispatcher.CurrentDispatcher

        # Check the version of windows and make sure we are setting the DPI mode
        # with the most up to date API
        # Windows Versioning Check Sources : https://www.lifewire.com/windows-version-numbers-2625171
        # and https://docs.microsoft.com/en-us/windows/release-information/
        win_version = Environment.OSVersion.Version
        if win_version.Major >= 6:  # Checks for Windows Vista or later
            # Represents Windows 8.1 up to Windows 10 before Build 1703 which should use
            # SetProcessDpiAwareness(True)
            if (win_version.Major == 6 and win_version.Minor == 3) or (
                win_version.Major == 10 and win_version.Build < 15063
            ):  # pragma: no cover
                windll.shcore.SetProcessDpiAwareness(True)
                print(
                    "WARNING: Your Windows version doesn't support DPI-independent rendering.  "
                    "We recommend you upgrade to at least Windows 10 Build 1703."
                )
            # Represents Windows 10 Build 1703 and beyond which should use
            # SetProcessDpiAwarenessContext(-2)
            elif win_version.Major == 10 and win_version.Build >= 15063:
                windll.user32.SetProcessDpiAwarenessContext(-2)
            # Any other version of windows should use SetProcessDPIAware()
            else:  # pragma: no cover
                windll.user32.SetProcessDPIAware()

        self.native.EnableVisualStyles()
        self.native.SetCompatibleTextRenderingDefault(False)

        # Ensure that TLS1.2 and TLS1.3 are enabled for HTTPS connections.
        # For some reason, some Windows installs have these protocols
        # turned off by default. SSL3, TLS1.0 and TLS1.1 are *not* enabled
        # as they are deprecated protocols and their use should *not* be
        # encouraged.
        try:
            ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12
        except AttributeError:  # pragma: no cover
            print(
                "WARNING: Your Windows .NET install does not support TLS1.2. "
                "You may experience difficulties accessing some web server content."
            )
        try:
            ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls13
        except AttributeError:  # pragma: no cover
            print(
                "WARNING: Your Windows .NET install does not support TLS1.3. "
                "You may experience difficulties accessing some web server content."
            )

        # Call user code to populate the main window
        self.interface._startup()

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_app_commands(self):
        # Set up the default commands for the interface.
        if (
            isinstance(self.interface.main_window, toga.MainWindow)
            or self.interface.main_window is None
        ):
            self.interface.commands.add(
                #
                toga.Command(
                    self.interface._menu_preferences,
                    "Preferences",
                    group=toga.Group.FILE,
                    # For now, only enable preferences if the user defines an implementation
                    enabled=overridden(self.interface.preferences),
                ),
                #
                # On Windows, the Exit command doesn't usually contain the app name. It
                # should be the last item in the File menu, in a section on its own.
                toga.Command(
                    self.interface._menu_exit,
                    "Exit",
                    shortcut=Key.MOD_1 + "q",
                    group=toga.Group.FILE,
                    section=sys.maxsize,
                ),
                #
                toga.Command(
                    self.interface._menu_visit_homepage,
                    "Visit homepage",
                    enabled=self.interface.home_page is not None,
                    group=toga.Group.HELP,
                ),
                # About should be the last item in the Help menu, in a section on its own.
                toga.Command(
                    self.interface._menu_about,
                    f"About {self.interface.formal_name}",
                    group=toga.Group.HELP,
                    section=sys.maxsize,
                ),
            )

        # Add a "New" menu item for each unique registered document type.
        if self.interface.document_types:
            for document_class in self.interface.document_types.values():
                self.interface.commands.add(
                    toga.Command(
                        self.interface._menu_new_document(document_class),
                        text=f"New {document_class.document_type}",
                        shortcut=(
                            toga.Key.MOD_1 + "n"
                            if document_class == self.interface.main_window
                            else None
                        ),
                        group=toga.Group.FILE,
                        section=0,
                    ),
                )

        # If there's a user-provided open() implementation, or there are registered
        # document types, add an Open menu item.
        if overridden(self.interface.open) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_open_file,
                    text="Open\u2026",
                    shortcut=toga.Key.MOD_1 + "o",
                    group=toga.Group.FILE,
                    section=10,
                ),
            )

        # If there is a user-provided save() implementation, or there are registered
        # document types, add a Save menu item.
        if overridden(self.interface.save) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_save,
                    text="Save",
                    shortcut=toga.Key.MOD_1 + "s",
                    group=toga.Group.FILE,
                    section=20,
                ),
            )

        # If there is a user-provided save_as() implementation, or there are registered
        # document types, add a Save As menu item.
        if overridden(self.interface.save_as) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_save_as,
                    text="Save As\u2026",
                    group=toga.Group.FILE,
                    section=20,
                    order=10,
                ),
            )

        # If there is a user-provided save_all() implementation, or there are registered
        # document types, add a Save All menu item.
        if overridden(self.interface.save_all) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_save_all,
                    text="Save All",
                    group=toga.Group.FILE,
                    section=20,
                    order=20,
                ),
            )

    def create_menus(self):
        for window in self.interface.windows:
            window._impl.create_menus()

    ######################################################################
    # App lifecycle
    ######################################################################

    def exit(self):  # pragma: no cover
        self._is_exiting = True
        self.native.Exit()

    def finalize(self):
        self.create_app_commands()
        self.create_menus()

        # Process any command line arguments to open documents, etc
        self.interface._create_initial_windows()

    def _run_app(self):  # pragma: no cover
        # Enable coverage tracing on this non-Python-created thread
        # (https://github.com/nedbat/coveragepy/issues/686).
        if threading._trace_hook:
            sys.settrace(threading._trace_hook)

        try:
            self.create()

            # This catches errors in handlers, and prints them
            # in a usable form.
            self.native.ThreadException += WeakrefCallable(winforms_thread_exception)

            self.loop.run_forever(self)
        except Exception as e:
            # In case of an unhandled error at the level of the app,
            # preserve the Python stacktrace
            self._exception = e
        else:
            self._exception = None

    def main_loop(self):
        thread = Threading.Thread(Threading.ThreadStart(self._run_app))
        thread.SetApartmentState(Threading.ApartmentState.STA)
        thread.Start()
        thread.Join()

        # If the thread has exited, the _exception attribute will exist.
        # If it's non-None, raise it, as it indicates the underlying
        # app thread had a problem; this is effectibely a re-raise over
        # a thread boundary.
        if self._exception:  # pragma: no cover
            raise self._exception

    def set_main_window(self, window):
        if isinstance(window, toga.Window):
            self.app_context.MainForm = window._impl.native

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        primary_screen = ScreenImpl(WinForms.Screen.PrimaryScreen)
        screen_list = [primary_screen] + [
            ScreenImpl(native=screen)
            for screen in WinForms.Screen.AllScreens
            if screen != primary_screen.native
        ]
        return screen_list

    ######################################################################
    # App capabilities
    ######################################################################

    def beep(self):
        SystemSounds.Beep.Play()

    def show_about_dialog(self):
        message_parts = []
        if self.interface.version is not None:
            message_parts.append(
                f"{self.interface.formal_name} v{self.interface.version}"
            )
        else:
            message_parts.append(self.interface.formal_name)

        if self.interface.author is not None:
            message_parts.append(f"Author: {self.interface.author}")
        if self.interface.description is not None:
            message_parts.append(f"\n{self.interface.description}")
        self.interface.main_window.info_dialog(
            f"About {self.interface.formal_name}", "\n".join(message_parts)
        )

    ######################################################################
    # Cursor control
    ######################################################################

    def hide_cursor(self):
        if self._cursor_visible:
            WinForms.Cursor.Hide()
        self._cursor_visible = False

    def show_cursor(self):
        if not self._cursor_visible:
            WinForms.Cursor.Show()
        self._cursor_visible = True

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        for window in self.interface.windows:
            if WinForms.Form.ActiveForm == window._impl.native:
                return window._impl
        return None

    def set_current_window(self, window):
        window._impl.native.Activate()

    ######################################################################
    # Full screen control
    ######################################################################

    def enter_full_screen(self, windows):
        for window in windows:
            window._impl.set_full_screen(True)

    def exit_full_screen(self, windows):
        for window in windows:
            window._impl.set_full_screen(False)


class DocumentApp(App):  # pragma: no cover
    def create_app_commands(self):
        super().create_app_commands()
        self.interface.commands.add(
            toga.Command(
                lambda w: self.open_file,
                text="Open...",
                shortcut=Key.MOD_1 + "o",
                group=toga.Group.FILE,
                section=0,
            ),
        )
