import asyncio
import os
import os.path
import signal
import sys
from urllib.parse import unquote, urlparse

import gbulb

import toga
from toga import App as toga_App
from toga.command import Command

from .libs import TOGA_DEFAULT_STYLES, Gdk, Gio, Gtk
from .window import Window


def gtk_menu_item_activate(cmd):
    """Convert a GTK menu item activation into a command invocation."""

    def _handler(action, data):
        cmd.action(cmd)

    return _handler


class MainWindow(Window):
    _IMPL_CLASS = Gtk.ApplicationWindow

    def __init__(self, interface, title, position, size):
        super().__init__(interface, title, position, size)
        icon_impl = toga_App.app.icon._impl
        self.native.set_icon_name(icon_impl.native_72.get_icon_name())

    def gtk_close_request(self, *args):
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
    This is the Gtk-backed implementation of the App interface class. It is
    the manager of all the other bits of the GUI app in Gtk-backend.
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
        self._create_app_commands()

        self.interface.startup()

        # Create the lookup table of menu items,
        # then force the creation of the menus.
        self.create_menus()

        # Set the default Toga styles
        css_provider = Gtk.CssProvider()

        # Backward compatibility fix for different gtk versions ===============
        if Gtk.get_major_version() >= 4 and Gtk.get_minor_version() >= 12:
            css_provider.load_from_string(TOGA_DEFAULT_STYLES)
        elif Gtk.get_major_version() >= 4 and Gtk.get_minor_version() > 8:
            css_provider.load_from_data(TOGA_DEFAULT_STYLES, len(TOGA_DEFAULT_STYLES))
        else:
            css_provider.load_from_data(TOGA_DEFAULT_STYLES.encode("utf-8"))
        # =====================================================================

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def _create_app_commands(self):
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

    def gtk_activate(self, data=None):
        pass

    def create_menus(self):
        # TODO: Implementing menus in HeaderBar; See #1931.
        self.interface.factory.not_implemented("Window.create_menus()")
        pass

    def _submenu(self, group, menubar):
        pass

    def main_loop(self):
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.loop.run_forever(application=self.native)

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        about = Gtk.AboutDialog()

        icon_impl = toga_App.app.icon._impl
        about.set_logo(icon_impl.native_72.get_paintable())

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

        about.set_modal(True)
        about.set_transient_for(self.get_current_window().native)
        about.present()

    def beep(self):
        Gdk.gdk_beep()

    def exit(self):
        self.native.quit()

    def set_on_exit(self, value):
        pass

    def get_current_window(self):
        return self.native.get_active_window()._impl

    def set_current_window(self, window):
        window._impl.native.present()

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
