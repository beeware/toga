import asyncio
import sys
import traceback

import toga
from toga.handlers import wrapped_handler

from .libs import Threading, WinForms, user32, win_version, shcore
from .libs.proactor import WinformsProactorEventLoop
from .window import Window


class MainWindow(Window):
    def on_close(self):
        pass


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.loop = WinformsProactorEventLoop()
        asyncio.set_event_loop(self.loop)

    def create(self):
        self.native = WinForms.Application
        self.app_context = WinForms.ApplicationContext()

        # Check the version of windows and make sure we are setting the DPI mode
        # with the most up to date API
        # Windows Versioning Check Sources : https://www.lifewire.com/windows-version-numbers-2625171
        # and https://docs.microsoft.com/en-us/windows/release-information/
        if win_version.Major >= 6:  # Checks for Windows Vista or later
            # Represents Windows 8.1 up to Windows 10 before Build 1703 which should use
            # SetProcessDpiAwareness(True)
            if ((win_version.Major == 6 and win_version.Minor == 3) or
                    (win_version.Major == 10 and win_version.Build < 15063)):
                shcore.SetProcessDpiAwareness(True)
            # Represents Windows 10 Build 1703 and beyond which should use
            # SetProcessDpiAwarenessContext(-2)
            elif win_version.Major == 10 and win_version.Build >= 15063:
                user32.SetProcessDpiAwarenessContext(-2)
            # Any other version of windows should use SetProcessDPIAware()
            else:
                user32.SetProcessDPIAware()

        self.native.EnableVisualStyles()
        self.native.SetCompatibleTextRenderingDefault(False)

        self.interface.commands.add(
            toga.Command(None, 'About ' + self.interface.name, group=toga.Group.HELP),
            toga.Command(None, 'Preferences', group=toga.Group.FILE),
            # Quit should always be the last item, in a section on it's own
            toga.Command(lambda s: self.exit(), 'Exit ' + self.interface.name, shortcut='q', group=toga.Group.FILE,
                         section=sys.maxsize),
            toga.Command(None, 'Visit homepage', group=toga.Group.HELP)
        )
        self._create_app_commands()

        # Call user code to populate the main window
        self.interface.startup()
        self._menu_items = {}
        self.create_menus()
        self.interface.main_window._impl.native.Icon = \
            self.interface.icon._impl.native

    def create_menus(self):
        toga.Group.FILE.order = 0
        # Only create the menu if the menu item index has been created.
        if hasattr(self, '_menu_items'):
            menubar = WinForms.MenuStrip()
            submenu = None
            for cmd in self.interface.commands:
                if cmd == toga.GROUP_BREAK:
                    menubar.Items.Add(submenu)
                    submenu = None
                elif cmd == toga.SECTION_BREAK:
                    submenu.DropDownItems.Add('-')
                else:
                    if submenu is None:
                        submenu = WinForms.ToolStripMenuItem(cmd.group.label)
                    item = WinForms.ToolStripMenuItem(cmd.label)
                    if cmd.action:
                        item.Click += cmd._impl.as_handler()
                    else:
                        item.Enabled = False
                    cmd._impl.native.append(item)
                    self._menu_items[item] = cmd
                    submenu.DropDownItems.Add(item)
            if submenu:
                menubar.Items.Add(submenu)
            self.interface.main_window._impl.native.Controls.Add(menubar)
            self.interface.main_window._impl.native.MainMenuStrip = menubar
        self.interface.main_window.content.refresh()

    def _create_app_commands(self):
        # No extra menus
        pass

    def open_document(self, fileURL):
        '''Add a new document to this app.'''
        print("STUB: If you want to handle opening documents, implement App.open_document(fileURL)")

    def app_exception_handler(self, sender, winforms_exc):
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
        tb_end_pos = py_exc.StackTrace.index("\\n']   at Python")
        tb_str = py_exc.StackTrace[2:tb_end_pos]
        for level in tb_str.split("', '"):
            for line in level.split("\\n"):
                if line:
                    print(line)
        print(py_exc.Message)

    def run_app(self):
        try:
            self.create()

            self.native.ThreadException += self.app_exception_handler
            self.native.ApplicationExit += self.app_exit_handler

            self.loop.run_forever(self.app_context)
        except:  # NOQA
            traceback.print_exc()

    def main_loop(self):
        thread = Threading.Thread(Threading.ThreadStart(self.run_app))
        thread.SetApartmentState(Threading.ApartmentState.STA)
        thread.Start()
        thread.Join()

    def app_exit_handler(self, sender, *args, **kwargs):
        pass

    def exit(self):
        self.native.Exit()

    def set_main_window(self, window):
        self.app_context.MainForm = window._impl.native

    def set_on_exit(self, value):
        pass

    def current_window(self):
        self.interface.factory.not_implemented('App.current_window()')

    def enter_full_screen(self, windows):
        self.interface.factory.not_implemented('App.enter_full_screen()')

    def exit_full_screen(self, windows):
        self.interface.factory.not_implemented('App.exit_full_screen()')

    def set_cursor(self, value):
        self.interface.factory.not_implemented('App.set_cursor()')

    def show_cursor(self):
        self.interface.factory.not_implemented('App.show_cursor()')

    def hide_cursor(self):
        self.interface.factory.not_implemented('App.hide_cursor()')

    def add_background_task(self, handler):
        self.loop.call_soon(wrapped_handler(self, handler), self)


class DocumentApp(App):
    def _create_app_commands(self):
        self.interface.commands.add(
            toga.Command(
                lambda w: self.open_file,
                label='Open...',
                shortcut='o',
                group=toga.Group.FILE,
                section=0
            ),
        )

    def open_document(self, fileURL):
        """Open a new document in this app.

        Args:
            fileURL (str): The URL/path to the file to add as a document.
        """
        self.interface.factory.not_implemented('DocumentApp.open_document()')
