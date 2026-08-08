from win32more import String
from win32more.Microsoft.UI.Input import InputSystemCursor, InputSystemCursorShape
from win32more.Microsoft.UI.Windowing import DisplayArea
from win32more.Microsoft.UI.Xaml import ApplicationTheme
from win32more.Windows.Win32.Media.Audio import SND_ALIAS, SND_ASYNC, PlaySound
from win32more.Windows.Win32.UI.WindowsAndMessaging import ShowCursor

from .libs.nativeapp import NativeApp
from .libs.proactor import WinUI3ProactorEventLoop
from .screens import Screen as ScreenImpl


class App:
    # Windows applications exit when the last window is closed.
    CLOSE_ON_LAST_WINDOW = True
    # Windows applications use default command line handling.
    HANDLES_COMMAND_LINE = False

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        # Track whether the app is exiting.
        self._is_exiting = False
        self._exiting_presentation = False
        self._cursor_visible = True

        self.loop = WinUI3ProactorEventLoop()
        self.native_instance: NativeApp

    def create(self):
        self.native = NativeApp

        # TODO Ensure that TLS1.2 and TLS1.3 are enabled. See Winforms.

        # Populate the main window as soon as the event loop is running.
        self.loop.call_soon_threadsafe(self.interface._startup)

    ####################################################################################
    # Commands and menus
    ####################################################################################

    def create_standard_commands(self):
        # The standard commands for WinUI 3 are already created by the Toga core
        # interface by calling _create_standard_commands() during _startup().
        pass

    def create_menus(self):
        """Creates menu bars for the windows with the 'create_menus' attribute."""
        for window in self.interface.windows:
            # It's difficult to trigger this on a simple window, because we can't easily
            # modify the set of app-level commands that are registered, and a simple
            # window doesn't exist when the app starts up. Therefore, no-branch the else
            # case.
            if hasattr(window._impl, "create_menus"):  # pragma: no branch
                window._impl.create_menus()

    ####################################################################################
    # App lifecycle
    ####################################################################################

    def exit(self):  # pragma: no cover
        self._is_exiting = True

    def main_loop(self):
        self.create()
        self.loop.run_forever(self)

    def set_icon(self, icon):
        for window in self.interface.windows:
            window._impl.set_app(self)

    def set_main_window(self, window):
        # Everything is already handled by the Toga core interface.
        pass

    ####################################################################################
    # App resources
    ####################################################################################

    def get_primary_screen(self):
        """Returns the WinUI 3 Screen object for the primary screen."""
        return ScreenImpl(DisplayArea.Primary)

    def get_screens(self):
        """Gets a list of WinUI 3 Screen objects corresponding to the system's screens.

        The primary screen has index 0 within the returned list.
        """
        primary_screen = self.get_primary_screen()
        screen_list = [primary_screen] + [
            ScreenImpl(native=screen)
            for screen in DisplayArea.FindAll()
            if ScreenImpl(native=screen) != primary_screen
        ]
        return screen_list

    ####################################################################################
    # App state
    ####################################################################################

    def get_dark_mode_state(self) -> bool:
        """Returns True if the NativeApp instance is in dark mode."""
        return self.native_instance.RequestedTheme == ApplicationTheme.Dark

    ####################################################################################
    # App capabilities
    ####################################################################################

    def beep(self):
        """Plays the 'SystemAsterisk' sound."""
        # learn.microsoft.com/windows/win32/multimedia/the-playsound-function
        PlaySound(String("SystemAsterisk"), None, SND_ALIAS | SND_ASYNC)

    def show_about_dialog(self):
        self.interface.factory.not_implemented("App.show_about_dialog")

    ####################################################################################
    # Cursor control
    #
    # To show/hide the cursor for the entire app, a combination of the Win32 function
    # ShowCursor and the WinUI 3 property ProtectedCursor is used:
    #   - ShowCursor: Only works on the non-client area i.e. title bar, etc.
    #   - ProtectedCursor: Only works on UIElement descendants  e.g. Panels.
    #
    ####################################################################################

    def hide_cursor(self):
        if not self._cursor_visible:
            return

        self._cursor_visible = False
        ShowCursor(False)

        for window in self.interface.windows:
            # The idea to hide the cursor by disposing of it comes from:
            # https://github.com/microsoft/WindowsAppSDK/discussions/3601
            placeholder_cursor = InputSystemCursor.Create(InputSystemCursorShape.Arrow)
            window._impl.native.Content.ProtectedCursor = placeholder_cursor
            placeholder_cursor.Close()

    def show_cursor(self):
        if self._cursor_visible:
            return

        self._cursor_visible = True
        ShowCursor(True)

        for window in self.interface.windows:
            window._impl.native.Content.ProtectedCursor = None

    ####################################################################################
    # Window control
    ####################################################################################

    def get_current_window(self):
        """Returns the currently activated window if one exists, otherwise None."""
        for window in self.interface.windows:
            if window._impl.is_activated:
                return window._impl
        return None

    def set_current_window(self, window):
        """Brings a given window to the foreground and gives it input focus."""
        window._impl.native.Activate()
