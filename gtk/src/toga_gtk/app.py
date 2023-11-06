import asyncio
import signal
import sys
from pathlib import Path

import gbulb

import toga
from toga import App as toga_App
from toga.command import Command

from .libs import TOGA_DEFAULT_STYLES, Gdk, Gio, Gtk
from .window import Window


def gtk_menu_item_activate(cmd):
    """Convert a GTK menu item activation into a command invocation."""

    def _handler(action, data):
        cmd.action()

    return _handler


class MainWindow(Window):
    def create(self):
        self.native = Gtk.ApplicationWindow()
        self.native.set_role("MainWindow")
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
        self.interface.app.on_exit()
        return True


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
        self.native_about_dialog = None

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
                self._menu_about,
                "About " + self.interface.formal_name,
                group=toga.Group.HELP,
            ),
            Command(None, "Preferences", group=toga.Group.APP),
            # Quit should always be the last item, in a section on its own
            Command(
                self._menu_quit,
                "Quit " + self.interface.formal_name,
                shortcut=toga.Key.MOD_1 + "q",
                group=toga.Group.APP,
                section=sys.maxsize,
            ),
        )

    def gtk_activate(self, data=None):
        pass

    def _menu_about(self, app, **kwargs):
        self.interface.about()

    def _menu_quit(self, app, **kwargs):
        self.interface.on_exit()

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
        self.native_about_dialog = Gtk.AboutDialog()
        self.native_about_dialog.set_modal(True)
        self.native_about_dialog.set_transient_for(self.get_current_window().native)

        icon_impl = toga_App.app.icon._impl
        self.native_about_dialog.set_logo(icon_impl.native_72.get_paintable())

        self.native_about_dialog.set_program_name(self.interface.formal_name)
        if self.interface.version is not None:
            self.native_about_dialog.set_version(self.interface.version)
        if self.interface.author is not None:
            self.native_about_dialog.set_authors([self.interface.author])
        if self.interface.description is not None:
            self.native_about_dialog.set_comments(self.interface.description)
        if self.interface.home_page is not None:
            self.native_about_dialog.set_website(self.interface.home_page)

        self.native_about_dialog.present()

    def beep(self):
        Gdk.beep()

    # We can't call this under test conditions, because it would kill the test harness
    def exit(self):  # pragma: no cover
        self.native.quit()

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


class DocumentApp(App):  # pragma: no cover
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
            self.interface._open(Path(sys.argv[1]))
        except IndexError:
            # Nothing on the command line; open a file dialog instead.
            # Create a temporary window so we have context for the dialog
            m = toga.Window()
            m.open_file_dialog(
                self.interface.formal_name,
                file_types=self.interface.document_types.keys(),
                on_result=lambda dialog, path: self.interface._open(path)
                if path
                else self.exit(),
            )

    def open_file(self, widget, **kwargs):
        # Create a temporary window so we have context for the dialog
        m = toga.Window()
        m.open_file_dialog(
            self.interface.formal_name,
            file_types=self.interface.document_types.keys(),
            on_result=lambda dialog, path: self.interface._open(path) if path else None,
        )
