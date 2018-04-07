from .libs import Threading, WinForms
from .window import Window
import toga
import sys


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

        self.interface.commands.add(
            toga.Command(None, 'About ' + self.interface.name, group=toga.Group.HELP),
            toga.Command(None, 'Preferences', group=toga.Group.FILE),
            # Quit should always be the last item, in a section on it's own
            toga.Command(lambda s: self.exit(), 'Exit ' + self.interface.name, shortcut='q', group=toga.Group.FILE,
                         section=sys.maxsize),
            toga.Command(None, 'Visit homepage', group=toga.Group.HELP)
        )

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
                    item.Click += add_handler(cmd)
                    cmd._widgets.append(item)
                    self._menu_items[item] = cmd
                    # This line may appear redundant, but it triggers the logic
                    # to force the enabled status on the underlying widgets.
                    cmd.enabled = cmd.enabled
                    submenu.DropDownItems.Add(item)
            if submenu:
                menubar.Items.Add(submenu)

            self.interface.main_window._impl.native.Controls.Add(menubar)
            


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
