import asyncio
import os
import signal
import sys

import gbulb

import toga
from toga.app import overridden
from toga.command import Command, Separator

from .keys import gtk_accel
from .libs import TOGA_DEFAULT_STYLES, Gdk, Gio, GLib, Gtk
from .screens import Screen as ScreenImpl


class App:
    # GTK apps exit when the last window is closed
    CLOSE_ON_LAST_WINDOW = True

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        gbulb.install(gtk=True)
        self.loop = asyncio.new_event_loop()

        # Stimulate the build of the app
        self.native = Gtk.Application(
            application_id=self.interface.app_id,
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.native_about_dialog = None

        # Connect the GTK signal that will cause app startup to occur
        self.native.connect("startup", self.gtk_startup)
        # Activate is a no-op, but GTK complains if you don't implement it
        self.native.connect("activate", self.gtk_activate)

        self.actions = None

    def gtk_activate(self, data=None):
        pass

    def gtk_startup(self, data=None):
        self.interface._startup()

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_app_commands(self):
        # Set up the default commands for the interface.
        if (
            isinstance(self.interface.main_window, toga.MainWindow)
            or self.interface.main_window is None
        ):
            self.interface.commands.add(
                Command(
                    self.interface._menu_about,
                    "About " + self.interface.formal_name,
                    group=toga.Group.HELP,
                ),
                Command(
                    self.interface._menu_visit_homepage,
                    "Visit homepage",
                    enabled=self.interface.home_page is not None,
                    group=toga.Group.HELP,
                ),
                # Preferences should be the last section of the edit menu.
                Command(
                    self.interface._menu_preferences,
                    "Preferences",
                    group=toga.Group.EDIT,
                    section=sys.maxsize,
                    # For now, only enable preferences if the user defines an implementation
                    enabled=overridden(self.interface.preferences),
                ),
                # Quit should always be the last item, in a section on its own
                Command(
                    self.interface._menu_exit,
                    "Quit",
                    shortcut=toga.Key.MOD_1 + "q",
                    group=toga.Group.FILE,
                    section=sys.maxsize,
                ),
            )

        # Add a "New" menu item for each unique registered document type.
        if self.interface.document_types:
            for document_class in self.interface.document_types.values():
                self.interface.commands.add(
                    toga.Command(
                        self.interface._menu_new_document(document_class),
                        text=f"New {document_class.document_type}",
                        shortcut=(
                            toga.Key.MOD_1 + "n"
                            if document_class == self.interface.main_window
                            else None
                        ),
                        group=toga.Group.FILE,
                        section=0,
                    ),
                )

        # If there's a user-provided open() implementation, or there are registered
        # document types, add an Open menu item.
        if overridden(self.interface.open) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_open_file,
                    text="Open\u2026",
                    shortcut=toga.Key.MOD_1 + "o",
                    group=toga.Group.FILE,
                    section=10,
                ),
            )

        # If there is a user-provided save() implementation, or there are registered
        # document types, add a Save menu item.
        if overridden(self.interface.save) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_save,
                    text="Save",
                    shortcut=toga.Key.MOD_1 + "s",
                    group=toga.Group.FILE,
                    section=20,
                ),
            )

        # If there is a user-provided save_as() implementation, or there are registered
        # document types, add a Save As menu item.
        if overridden(self.interface.save_as) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_save_as,
                    text="Save As\u2026",
                    group=toga.Group.FILE,
                    section=20,
                    order=10,
                ),
            )

        # If there is a user-provided save_all() implementation, or there are registered
        # document types, add a Save All menu item.
        if overridden(self.interface.save_all) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_save_all,
                    text="Save All",
                    group=toga.Group.FILE,
                    section=20,
                    order=20,
                ),
            )

    def _submenu(self, group, menubar):
        try:
            submenu, section = self._menu_groups[group]
        except KeyError:
            # It's a new menu/group, so it must start a new section.
            section = Gio.Menu()
            if group is None:
                # Menu is a top-level menu; so it's a child of the menu bar
                submenu = menubar
            else:
                _, parent_section = self._submenu(group.parent, menubar)
                submenu = Gio.Menu()

                text = group.text
                if text == "*":
                    text = self.interface.formal_name
                parent_section.append_submenu(text, submenu)

            # Add the initial section to the submenu,
            # and install the menu item in the group cache.
            submenu.append_section(None, section)
            self._menu_groups[group] = submenu, section

        return submenu, section

    def create_menus(self):
        # Only create the menu if the menu item index has been created.
        self._menu_items = {}
        self._menu_groups = {}

        # Create the menu for the top level menubar.
        menubar = Gio.Menu()
        for cmd in self.interface.commands:
            submenu, section = self._submenu(cmd.group, menubar)
            if isinstance(cmd, Separator):
                section = Gio.Menu()
                submenu.append_section(None, section)
                self._menu_groups[cmd.group] = (submenu, section)
            else:
                cmd_id = "command-%s" % id(cmd)
                action = Gio.SimpleAction.new(cmd_id, None)
                action.connect("activate", cmd._impl.gtk_activate)

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

        # Now that we have menus, make the app take responsibility for
        # showing the menubar.
        # This is required because of inconsistencies in how the Gnome
        # shell operates on different windowing environments;
        # see #872 for details.
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-shell-shows-menubar", False)

    ######################################################################
    # App lifecycle
    ######################################################################

    # We can't call this under test conditions, because it would kill the test harness
    def exit(self):  # pragma: no cover
        self.native.quit()

    def finalize(self):
        # Set any custom styles
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(TOGA_DEFAULT_STYLES)

        context = Gtk.StyleContext()
        context.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        # Create the app commands and populate app menus.
        self.create_app_commands()
        self.create_menus()

        # Process any command line arguments to open documents, etc
        self.interface._create_initial_windows()

    def main_loop(self):
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Retain a reference to the app so that no-window apps can exist
        self.native.hold()

        self.loop.run_forever(application=self.native)

        # Release the reference to the app
        self.native.release()

    def set_main_window(self, window):
        if isinstance(window, toga.Window):
            window._impl.native.set_role("MainWindow")

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        display = Gdk.Display.get_default()
        if "WAYLAND_DISPLAY" in os.environ:  # pragma: no cover
            # `get_primary_monitor()` doesn't work on wayland, so return as it is.
            return [
                ScreenImpl(native=display.get_monitor(i))
                for i in range(display.get_n_monitors())
            ]
        else:
            primary_screen = ScreenImpl(display.get_primary_monitor())
            screen_list = [primary_screen] + [
                ScreenImpl(native=display.get_monitor(i))
                for i in range(display.get_n_monitors())
                if display.get_monitor(i) != primary_screen.native
            ]
            return screen_list

    ######################################################################
    # App capabilities
    ######################################################################

    def beep(self):
        Gdk.beep()

    def _close_about(self, dialog, *args):
        self.native_about_dialog.destroy()
        self.native_about_dialog = None

    def show_about_dialog(self):
        self.native_about_dialog = Gtk.AboutDialog()
        self.native_about_dialog.set_modal(True)

        icon_impl = toga.App.app.icon._impl
        self.native_about_dialog.set_logo(icon_impl.native_72)

        self.native_about_dialog.set_program_name(self.interface.formal_name)
        if self.interface.version is not None:
            self.native_about_dialog.set_version(self.interface.version)
        if self.interface.author is not None:
            self.native_about_dialog.set_authors([self.interface.author])
        if self.interface.description is not None:
            self.native_about_dialog.set_comments(self.interface.description)
        if self.interface.home_page is not None:
            self.native_about_dialog.set_website(self.interface.home_page)

        self.native_about_dialog.show()
        self.native_about_dialog.connect("close", self._close_about)
        self.native_about_dialog.connect("response", self._close_about)

    ######################################################################
    # Cursor control
    ######################################################################

    def hide_cursor(self):
        self.interface.factory.not_implemented("App.hide_cursor()")

    def show_cursor(self):
        self.interface.factory.not_implemented("App.show_cursor()")

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        current_window = self.native.get_active_window()._impl
        return current_window if current_window.interface.visible else None

    def set_current_window(self, window):
        window._impl.native.present()

    ######################################################################
    # Full screen control
    ######################################################################

    def enter_full_screen(self, windows):
        for window in windows:
            window._impl.set_full_screen(True)

    def exit_full_screen(self, windows):
        for window in windows:
            window._impl.set_full_screen(False)
