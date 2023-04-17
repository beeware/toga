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
from .libs import TOGA_DEFAULT_STYLES, Gdk, Gio, GLib, Gtk
from .window import Window


def gtk_menu_item_activate(cmd):
    """Convert a GTK menu item activation into a command invocation."""

    def _handler(action, data):
        cmd.action(cmd)

    return _handler


class MainWindow(Window):
    _IMPL_CLASS = Gtk.ApplicationWindow

    def create(self):
        super().create()
        self.native.set_role("MainWindow")
        icon_impl = toga_App.app.icon._impl
        self.native.set_icon(icon_impl.native_72.get_pixbuf())

    def gtk_delete_event(self, *args):
        # Return value of the GTK on_close handler indicates
        # whether the event has been fully handled. Returning
        # False indicates the event handling is *not* complete,
        # so further event processing (including actually
        # closing the window) should be performed; so
        # "should_exit == True" must be converted to a return
        # value of False.
        return not self.interface.app.exit()


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
        self.loop = asyncio.new_event_loop()

        self.create()

    def create(self):
        # Stimulate the build of the app
        self.native = Gtk.Application(
            application_id=self.interface.app_id,
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )

        # Connect the GTK signal that will cause app startup to occur
        self.native.connect("startup", self.gtk_startup)
        self.native.connect("activate", self.gtk_activate)

        self.actions = None

    def gtk_startup(self, data=None):
        # Set up the default commands for the interface.
        self.interface.commands.add(
            Command(
                lambda _: self.interface.about(),
                "About " + self.interface.name,
                group=toga.Group.HELP,
            ),
            Command(None, "Preferences", group=toga.Group.APP),
            # Quit should always be the last item, in a section on its own
            Command(
                lambda _: self.interface.exit(),
                "Quit " + self.interface.name,
                shortcut=toga.Key.MOD_1 + "q",
                group=toga.Group.APP,
                section=sys.maxsize,
            ),
        )
        self._create_app_commands()

        self.interface.startup()

        # Create the lookup table of menu items,
        # then force the creation of the menus.
        self.create_menus()

        # Now that we have menus, make the app take responsibility for
        # showing the menubar.
        # This is required because of inconsistencies in how the Gnome
        # shell operates on different windowing environments;
        # see #872 for details.
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-shell-shows-menubar", False)

        # Set any custom styles
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(TOGA_DEFAULT_STYLES)

        context = Gtk.StyleContext()
        context.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def _create_app_commands(self):
        # No extra menus
        pass

    def gtk_activate(self, data=None):
        pass

    def create_menus(self):
        # Only create the menu if the menu item index has been created.
        self._menu_items = {}
        self._menu_groups = {}

        # Create the menu for the top level menubar.
        menubar = Gio.Menu()
        section = None
        for cmd in self.interface.commands:
            if cmd == GROUP_BREAK:
                section = None
            elif cmd == SECTION_BREAK:
                section = None
            else:
                submenu = self._submenu(cmd.group, menubar)

                if section is None:
                    section = Gio.Menu()
                    submenu.append_section(None, section)

                cmd_id = "command-%s" % id(cmd)
                action = Gio.SimpleAction.new(cmd_id, None)
                if cmd.action:
                    action.connect("activate", gtk_menu_item_activate(cmd))

                cmd._impl.native.append(action)
                cmd._impl.set_enabled(cmd.enabled)
                self._menu_items[action] = cmd
                self.native.add_action(action)

                item = Gio.MenuItem.new(cmd.text, "app." + cmd_id)
                if cmd.shortcut:
                    item.set_attribute_value(
                        "accel", GLib.Variant("s", gtk_accel(cmd.shortcut))
                    )

                section.append_item(item)

        # Set the menu for the app.
        self.native.set_menubar(menubar)

    def _submenu(self, group, menubar):
        try:
            return self._menu_groups[group]
        except KeyError:
            if group is None:
                submenu = menubar
            else:
                parent_menu = self._submenu(group.parent, menubar)

                submenu = Gio.Menu()
                self._menu_groups[group] = submenu

                text = group.text
                if text == "*":
                    text = self.interface.name

                parent_menu.append_submenu(text, submenu)

            # Install the item in the group cache.
            self._menu_groups[group] = submenu

            return submenu

    def main_loop(self):
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.loop.run_forever(application=self.native)

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        about = Gtk.AboutDialog()

        icon_impl = toga_App.app.icon._impl
        about.set_logo(icon_impl.native_72.get_pixbuf())

        if self.interface.name is not None:
            about.set_program_name(self.interface.name)
        if self.interface.version is not None:
            about.set_version(self.interface.version)
        if self.interface.author is not None:
            about.set_authors([self.interface.author])
        if self.interface.description is not None:
            about.set_comments(self.interface.description)
        if self.interface.home_page is not None:
            about.set_website(self.interface.home_page)

        about.run()
        about.destroy()

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
        self.interface.factory.not_implemented("App.show_cursor()")

    def hide_cursor(self):
        self.interface.factory.not_implemented("App.hide_cursor()")


class DocumentApp(App):
    def _create_app_commands(self):
        self.interface.commands.add(
            toga.Command(
                self.open_file,
                text="Open...",
                shortcut=toga.Key.MOD_1 + "o",
                group=toga.Group.FILE,
                section=0,
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
        fileURL = fileURL.rstrip("/")
        path = unquote(urlparse(fileURL).path)
        extension = os.path.splitext(path)[1][1:]

        # Create the document instance
        DocType = self.interface.document_types[extension]
        document = DocType(fileURL, self.interface)
        self.interface._documents.append(document)

        document.show()
