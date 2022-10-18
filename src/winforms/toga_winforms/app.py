import asyncio
import re
import sys

import toga
from toga import Key
from .keys import toga_to_winforms_key

from .libs import (
    SecurityProtocolType,
    ServicePointManager,
    Threading,
    WinForms,
    shcore,
    user32,
    win_version
)
from .libs.proactor import WinformsProactorEventLoop
from .window import Window


class MainWindow(Window):
    def winforms_FormClosing(self, sender, event):
        # Differentiate between the handling that occurs when the user
        # requests the app to exit, and the actual application exiting.
        if not self.interface.app._impl._is_exiting:
            # If there's an event handler, process it. The decision to
            # actually exit the app will be processed in the on_exit handler.
            # If there's no exit handler, assume the close/exit can proceed.
            if self.interface.app.on_exit:
                self.interface.app.on_exit(self.interface.app)
                event.Cancel = True


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        # Winforms app exit is tightly bound to the close of the MainWindow.
        # The FormClosing message on MainWindow triggers the "on_exit" handler
        # (which might abort the exit). However, on success, it will request the
        # app (and thus the Main Window) to close, causing another close event.
        # So - we have a flag that is only ever sent once a request has been
        # made to exit the native app. This flag can be used to shortcut any
        # window-level close handling.
        self._is_exiting = False

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

        # Ensure that TLS1.2 and TLS1.3 are enabled for HTTPS connections.
        # For some reason, some Windows installs have these protocols
        # turned off by default. SSL3, TLS1.0 and TLS1.1 are *not* enabled
        # as they are deprecated protocols and their use should *not* be
        # encouraged.
        try:
            ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12
        except AttributeError:
            print(
                "WARNING: Your Windows .NET install does not support TLS1.2. "
                "You may experience difficulties accessing some web server content."
            )
        try:
            ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls13
        except AttributeError:
            print(
                "WARNING: Your Windows .NET install does not support TLS1.3. "
                "You may experience difficulties accessing some web server content."
            )

        self.interface.commands.add(
            toga.Command(
                lambda _: self.interface.about(),
                'About {}'.format(self.interface.name),
                group=toga.Group.HELP
            ),
            toga.Command(None, 'Preferences', group=toga.Group.FILE),
            # Quit should always be the last item, in a section on it's own
            toga.Command(
                lambda _: self.interface.exit(),
                'Exit ' + self.interface.name,
                shortcut=Key.MOD_1 + 'q',
                group=toga.Group.FILE,
                section=sys.maxsize
            ),
            toga.Command(
                lambda _: self.interface.visit_homepage(),
                'Visit homepage',
                enabled=self.interface.home_page is not None,
                group=toga.Group.HELP
            )
        )
        self._create_app_commands()

        # Call user code to populate the main window
        self.interface.startup()
        self.create_menus()
        self.interface.icon.bind(self.interface.factory)
        self.interface.main_window._impl.set_app(self)

    def create_menus(self):
        self._menu_items = {}
        self._menu_groups = {}

        toga.Group.FILE.order = 0
        menubar = WinForms.MenuStrip()
        submenu = None
        for cmd in self.interface.commands:
            if cmd == toga.GROUP_BREAK:
                submenu = None
            elif cmd == toga.SECTION_BREAK:
                submenu.DropDownItems.Add('-')
            else:
                submenu = self._submenu(cmd.group, menubar)

                item = WinForms.ToolStripMenuItem(cmd.text)

                if cmd.action:
                    item.Click += cmd._impl.as_handler()
                item.Enabled = cmd.enabled

                if cmd.shortcut is not None:
                    shortcut_keys = toga_to_winforms_key(cmd.shortcut)
                    item.ShortcutKeys = shortcut_keys
                    item.ShowShortcutKeys = True

                cmd._impl.native.append(item)

                self._menu_items[item] = cmd
                submenu.DropDownItems.Add(item)

        self.interface.main_window._impl.native.Controls.Add(menubar)
        self.interface.main_window._impl.native.MainMenuStrip = menubar
        self.interface.main_window.content.refresh()

    def _submenu(self, group, menubar):
        try:
            return self._menu_groups[group]
        except KeyError:
            if group is None:
                submenu = menubar
            else:
                parent_menu = self._submenu(group.parent, menubar)

                submenu = WinForms.ToolStripMenuItem(group.text)

                # Top level menus are added in a different way to submenus
                if group.parent is None:
                    parent_menu.Items.Add(submenu)
                else:
                    parent_menu.DropDownItems.Add(submenu)

            self._menu_groups[group] = submenu
        return submenu

    def _create_app_commands(self):
        # No extra menus
        pass

    def open_document(self, fileURL):
        '''Add a new document to this app.'''
        print("STUB: If you want to handle opening documents, implement App.open_document(fileURL)")

    def winforms_thread_exception(self, sender, winforms_exc):
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
            re.DOTALL | re.UNICODE
        )

        stacktrace_relevant_lines = regex.findall(full_stack_trace)
        if len(stacktrace_relevant_lines) == 0:
            self.print_stack_trace(full_stack_trace)
        else:
            for lines in stacktrace_relevant_lines:
                for line in lines:
                    self.print_stack_trace(line)
        print(py_exc.Message)

    @classmethod
    def print_stack_trace(cls, stack_trace_line):
        for level in stack_trace_line.split("', '"):
            for line in level.split("\\n"):
                if line:
                    print(line)

    def run_app(self):
        try:
            self.create()

            # This catches errors in handlers, and prints them
            # in a usable form.
            self.native.ThreadException += self.winforms_thread_exception

            self.loop.run_forever(self.app_context)
        except Exception as e:
            # In case of an unhandled error at the level of the app,
            # preserve the Python stacktrace
            self._exception = e
        else:
            self._exception = None

    def main_loop(self):
        thread = Threading.Thread(Threading.ThreadStart(self.run_app))
        thread.SetApartmentState(Threading.ApartmentState.STA)
        thread.Start()
        thread.Join()

        # If the thread has exited, the _exception attribute will exist.
        # If it's non-None, raise it, as it indicates the underlying
        # app thread had a problem; this is effectibely a re-raise over
        # a thread boundary.
        if self._exception:
            raise self._exception

    def show_about_dialog(self):
        message_parts = []
        if self.interface.name is not None:
            if self.interface.version is not None:
                message_parts.append(
                    "{name} v{version}".format(
                        name=self.interface.name,
                        version=self.interface.version,
                    )
                )
            else:
                message_parts.append(
                    "{name}".format(name=self.interface.name)
                )
        elif self.interface.version is not None:
            message_parts.append(
                "v{version}".format(version=self.interface.version)
            )

        if self.interface.author is not None:
            message_parts.append(
                "Author: {author}".format(author=self.interface.author)
            )
        if self.interface.description is not None:
            message_parts.append(
                "\n{description}".format(
                    description=self.interface.description
                )
            )
        self.interface.main_window.info_dialog(
            'About {}'.format(self.interface.name), "\n".join(message_parts)
        )

    def exit(self):
        self._is_exiting = True
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
        self.loop.call_soon(handler, self)


class DocumentApp(App):
    def _create_app_commands(self):
        self.interface.commands.add(
            toga.Command(
                lambda w: self.open_file,
                text='Open...',
                shortcut=Key.MOD_1 + 'o',
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
