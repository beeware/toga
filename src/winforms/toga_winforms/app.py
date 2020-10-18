import asyncio
import re
import sys
import traceback

import toga
from toga import Key
from toga.handlers import wrapped_handler
from .keys import toga_to_winforms_key

from .libs import Threading, WinForms, shcore, user32, win_version
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
        self._data_menu_items = {}
        self._menu_groups = {}
        self._menubar = WinForms.MenuStrip()

        toga.Group.FILE.order = 0
        previous_command = None
        for cmd in self.interface.commands:
            if cmd == toga.GROUP_BREAK:
                continue
            elif cmd == toga.SECTION_BREAK:
                submenu = self._submenu(previous_command.group)
                submenu.DropDownItems.Add('-')
            else:
                self._menu_items[cmd] = self._add_command(cmd)
                previous_command = cmd

        self.interface.main_window._impl.native.Controls.Add(self._menubar)
        self.interface.main_window._impl.native.MainMenuStrip = self._menubar
        self.interface.main_window.content.refresh()

    def _create_app_commands(self):
        # No extra menus
        pass

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

            self.native.ThreadException += self.winforms_thread_exception
            self.native.ApplicationExit += self.winforms_application_exit

            self.loop.run_forever(self.app_context)
        except:  # NOQA
            traceback.print_exc()

    def main_loop(self):
        thread = Threading.Thread(Threading.ThreadStart(self.run_app))
        thread.SetApartmentState(Threading.ApartmentState.STA)
        thread.Start()
        thread.Join()

    def winforms_application_exit(self, sender, *args, **kwargs):
        pass

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

    def _add_command(self, command):
        submenu = self._submenu(command.group)
        submenu.Enabled = True

        # If a command has a sub_group, it's a menu item that is used
        # as the insertion point for data-based menu items (e.g., recent files)
        # Register it as a submenu.
        if command.sub_group:
            item = self._submenu(command.sub_group)
        else:
            item = WinForms.ToolStripMenuItem(command.label)

        if command.action:
            item.Click += command._impl.as_handler()
        item.Enabled = command.enabled

        if command.shortcut is not None:
            shortcut_keys = toga_to_winforms_key(command.shortcut)
            item.ShortcutKeys = shortcut_keys
            item.ShowShortcutKeys = True

        command._impl.native.append(item)

        submenu.DropDownItems.Add(item)

        return item

    def _update_data_menu_items(self, commandset):
        """
        Update the menu items relating to a data source.

        :param commandset: The commandset that needs to be updated.
        """
        # Remove all existing menu items
        if commandset in self._data_menu_items:
            submenu = self._submenu(commandset.sub_group)
            for item in self._data_menu_items[commandset]:
                submenu.DropDownItems.Remove(item)

        # Reset the data menu items list, and re-create the items
        # based on the current contents of the data source.
        self._data_menu_items[commandset] = []
        for command in commandset:
            self._data_menu_items[commandset].append(self._add_command(command))

    def _submenu(self, group):
        if group is None:
            return self._menubar
        try:
            return self._menu_groups[group]
        except KeyError:
            pass
        parent_menu = self._submenu(group.parent)

        submenu = WinForms.ToolStripMenuItem(group.label)

        # Top level menus are added in a different way to submenus
        if group.parent is None:
            parent_menu.Items.Add(submenu)
        else:
            parent_menu.DropDownItems.Add(submenu)

        self._menu_groups[group] = submenu
        return submenu


class DocumentApp(App):
    def _create_app_commands(self):
        self.interface.commands.add(
            toga.Command(
                lambda w: self.interface.open_file(),
                label='Open...',
                shortcut=Key.MOD_1 + 'o',
                group=toga.Group.FILE,
                section=0,
                order=1
            ),
            toga.DataSourceCommandSet(
                label="Recent",
                data=self.interface.documents,
                item_to_label=lambda item: item.path.stem,
                group=toga.Group.FILE,
                section=0,
                order=2,
                item_action=lambda widget, item: self.interface.open_recent(item.path),
                app=self.interface,
            )
        )
