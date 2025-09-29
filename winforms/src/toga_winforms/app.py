import asyncio
import re
import sys
import threading

import System.Windows.Forms as WinForms
from Microsoft.Win32 import SystemEvents
from System import Threading
from System.Media import SystemSounds
from System.Net import SecurityProtocolType, ServicePointManager
from System.Windows.Threading import Dispatcher

from toga.dialogs import InfoDialog

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
    # Winforms apps use default command line handling
    HANDLES_COMMAND_LINE = False

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        # Track whether the app is exiting. This is used to stop the event loop,
        # and shortcut close handling on any open windows when the app exits.
        self._is_exiting = False

        # Winforms cursor visibility is a stack; If you call hide N times, you
        # need to call Show N times to make the cursor re-appear. Store a local
        # boolean to allow us to avoid building a deep stack.
        self._cursor_visible = True

        self.loop = WinformsProactorEventLoop()
        asyncio.set_event_loop(self.loop)

    def create(self):
        self.native = WinForms.Application
        self.app_context = WinForms.ApplicationContext()
        self.app_dispatcher = Dispatcher.CurrentDispatcher

        # We would prefer to detect DPI changes directly, using the DpiChanged,
        # DpiChangedBeforeParent or DpiChangedAfterParent events on the window. But none
        # of these events ever fire, possibly because we're missing some app metadata
        # (https://github.com/beeware/toga/pull/2155#issuecomment-2460374101). So
        # instead we need to listen to all events which could cause a DPI change:
        #   * DisplaySettingsChanged
        #   * Form.LocationChanged and Form.Resize, since a window's DPI is determined
        #     by which screen most of its area is on.
        SystemEvents.DisplaySettingsChanged += WeakrefCallable(
            self.winforms_DisplaySettingsChanged
        )

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

        # Populate the main window as soon as the event loop is running.
        self.loop.call_soon_threadsafe(self.interface._startup)

    ######################################################################
    # Native event handlers
    ######################################################################

    def winforms_DisplaySettingsChanged(self, sender, event):
        # This event is NOT called on the UI thread, so it's not safe for it to access
        # the UI directly.
        self.interface.loop.call_soon_threadsafe(self.update_dpi)

    def update_dpi(self):
        for window in self.interface.windows:
            window._impl.update_dpi()

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_standard_commands(self):
        pass

    def create_menus(self):
        # Winforms menus are created on the Window.
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

    def exit(self):  # pragma: no cover
        self._is_exiting = True
        self.native.Exit()

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
            # Ensure the event loop is fully closed.
            self.loop.close()
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

    def set_icon(self, icon):
        for window in self.interface.windows:
            window._impl.native.Icon = icon._impl.native

    def set_main_window(self, window):
        pass

    ######################################################################
    # App resources
    ######################################################################

    def get_primary_screen(self):
        return ScreenImpl(WinForms.Screen.PrimaryScreen)

    def get_screens(self):
        primary_screen = self.get_primary_screen()
        screen_list = [primary_screen] + [
            ScreenImpl(native=screen)
            for screen in WinForms.Screen.AllScreens
            if screen != primary_screen.native
        ]
        return screen_list

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
        asyncio.create_task(
            self.interface.dialog(
                InfoDialog(
                    f"About {self.interface.formal_name}", "\n".join(message_parts)
                )
            )
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
