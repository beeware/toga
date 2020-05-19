import asyncio
import os
import os.path
import signal
import sys
from urllib.parse import unquote, urlparse

import gbulb
import toga
from toga import App as toga_App
from toga.command import GROUP_BREAK, SECTION_BREAK, Command

from .keys import gtk_accel
from .libs import Gio, GLib, Gtk
from .window import Window


def gtk_menu_item_activate(cmd):
    """Convert a GTK menu item activation into a command invocation"""
    def _handler(action, data):
        cmd.action(cmd)
    return _handler


class MainWindow(Window):
    _IMPL_CLASS = Gtk.ApplicationWindow

    def create(self):
        super().create()
        self.native.set_role("MainWindow")
        toga_App.app.icon.bind(self.interface.factory)
        self.native.set_icon(toga_App.app.icon._impl.native_72.get_pixbuf())

    def set_app(self, app):
        super().set_app(app)

        # The GTK docs list set_wmclass() as deprecated (and "pointless")
        # but it's the only way I've found that actually sets the
        # Application name to something other than '__main__.py'.
        self.native.set_wmclass(app.interface.name, app.interface.name)

    def on_close(self, *args):
        pass


class App:
    """
    Todo:
        * Creation of Menus is not working.
        * Disabling of menu items is not working.
        * App Icon is not showing up
    """
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        gbulb.install(gtk=True)
        self.loop = asyncio.get_event_loop()

        self.create()

    def create(self):
        # Stimulate the build of the app
        self.native = Gtk.Application(
            application_id=self.interface.app_id,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        # Connect the GTK signal that will cause app startup to occur
        self.native.connect('startup', self.gtk_startup)
        self.native.connect('activate', self.gtk_activate)
        # self.native.connect('shutdown', self.shutdown)

        self.actions = None

    def gtk_startup(self, data=None):
        # Set up the default commands for the interface.
        self.interface.commands.add(
            Command(None, 'About ' + self.interface.name, group=toga.Group.HELP),
            Command(None, 'Preferences', group=toga.Group.APP),
            # Quit should always be the last item, in a section on it's own
            Command(
                lambda widget: self.exit(),
                'Quit ' + self.interface.name,
                shortcut=toga.Key.MOD_1 + 'q',
                group=toga.Group.APP,
                section=sys.maxsize
            ),
            Command(None, 'Visit homepage', group=toga.Group.HELP)
        )
        self._create_app_commands()

        self.interface.startup()

        # Create the lookup table of menu items,
        # then force the creation of the menus.
        self._actions = {}
        self.create_menus()

        # Now that we have menus, make the app take responsibility for
        # showing the menubar.
        # This is required because of inconsistencies in how the Gnome
        # shell operates on different windowing environments;
        # see #872 for details.
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-shell-shows-menubar", False)

    def _create_app_commands(self):
        # No extra menus
        pass

    def gtk_activate(self, data=None):
        pass

    def create_menus(self):
        # Only create the menu if the menu item index has been created.
        if hasattr(self, '_actions'):
            self._actions = {}
            menubar = Gio.Menu()
            label = None
            submenu = None
            section = None
            for cmd in self.interface.commands:
                if cmd == GROUP_BREAK:
                    if section:
                        submenu.append_section(None, section)

                    if label == '*':
                        label = self.interface.name
                    menubar.append_submenu(label, submenu)

                    label = None
                    submenu = None
                    section = None
                elif cmd == SECTION_BREAK:
                    submenu.append_section(None, section)
                    section = None

                else:
                    if submenu is None:
                        label = cmd.group.label
                        submenu = Gio.Menu()

                    if section is None:
                        section = Gio.Menu()

                    try:
                        action = self._actions[cmd]
                    except KeyError:
                        cmd_id = "command-%s" % id(cmd)
                        action = Gio.SimpleAction.new(cmd_id, None)
                        if cmd.action:
                            action.connect("activate", gtk_menu_item_activate(cmd))

                        cmd._impl.native.append(action)
                        cmd._impl.set_enabled(cmd.enabled)
                        self._actions[cmd] = action
                        self.native.add_action(action)

                    item = Gio.MenuItem.new(cmd.label, 'app.' + cmd_id)
                    if cmd.shortcut:
                        item.set_attribute_value('accel', GLib.Variant('s', gtk_accel(cmd.shortcut)))

                    section.append_item(item)

            if section:
                submenu.append_section(None, section)

            if submenu:
                if label == '*':
                    label = self.interface.name
                menubar.append_submenu(label, submenu)

            # Set the menu for the app.
            self.native.set_menubar(menubar)

    def main_loop(self):
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.loop.run_forever(application=self.native)

    def set_main_window(self, window):
        pass

    def exit(self):
        self.native.quit()

    def set_on_exit(self, value):
        pass

    def current_window(self):
        return self.native.get_active_window()._impl

    def enter_full_screen(self, windows):
        for window in windows:
            window._impl.set_full_screen(True)

    def exit_full_screen(self, windows):
        for window in windows:
            window._impl.set_full_screen(False)

    def show_cursor(self):
        self.interface.factory.not_implemented('App.show_cursor()')

    def hide_cursor(self):
        self.interface.factory.not_implemented('App.hide_cursor()')

    def add_background_task(self, handler):
        self.interface.factory.not_implemented('App.add_background_task()')


class DocumentApp(App):
    def _create_app_commands(self):
        self.interface.commands.add(
            toga.Command(
                self.open_file,
                label='Open...',
                shortcut=toga.Key.MOD_1 + 'o',
                group=toga.Group.FILE,
                section=0
            ),
        )

    def gtk_startup(self, data=None):
        super().gtk_startup(data=data)

        try:
            # Look for a filename specified on the command line
            file_name = os.path.abspath(sys.argv[1])
        except IndexError:
            # Nothing on the command line; open a file dialog instead.
            # TODO: This causes a blank window to be shown.
            # Is there a way to open a file dialog without having a window?
            m = toga.Window()
            file_name = m.select_folder_dialog(self.interface.name, None, False)[0]

        self.open_document(file_name)

    def open_file(self, widget, **kwargs):
        # TODO: This causes a blank window to be shown.
        # Is there a way to open a file dialog without having a window?
        m = toga.Window()
        file_name = m.select_folder_dialog(self.interface.name, None, False)[0]

        self.open_document(file_name)

    def open_document(self, fileURL):
        """Open a new document in this app.

        Args:
            fileURL (str): The URL/path to the file to add as a document.
        """
        # Convert the fileURL to a file path.
        fileURL = fileURL.rstrip('/')
        path = unquote(urlparse(fileURL).path)
        extension = os.path.splitext(path)[1][1:]

        # Create the document instance
        DocType = self.interface.document_types[extension]
        document = DocType(fileURL, self.interface)
        self.interface._documents.append(document)

        document.show()
