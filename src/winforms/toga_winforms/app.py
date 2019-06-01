import sys

import toga

from .libs import Threading, WinForms, add_handler, user32, win_version
from .window import Window


class MainWindow(Window):
    def on_close(self):
        pass


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def create(self):
        self.native = WinForms.Application

        if win_version >= 6:
            user32.SetProcessDPIAware(True)
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
            self.interface.icon.bind(self.interface.factory).native

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
                        item.Click += add_handler(cmd)
                    else:
                        item.Enabled = False
                    cmd._widgets.append(item)
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

    def run_app(self):
        self.create()
        self.native.Run(self.interface.main_window._impl.native)

    def main_loop(self):
        thread = Threading.Thread(Threading.ThreadStart(self.run_app))
        thread.SetApartmentState(Threading.ApartmentState.STA)
        thread.Start()
        thread.Join()

    def exit(self):
        self.native.Exit()

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
