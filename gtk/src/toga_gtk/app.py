import asyncio
import os
import signal
import sys

import gbulb

import toga
from toga.app import App as toga_App
from toga.command import Command, Group, Separator
from toga.handlers import overridden, simple_handler

from .keys import gtk_accel
from .libs import TOGA_DEFAULT_STYLES, Gdk, Gio, GLib, Gtk
from .screens import Screen as ScreenImpl


class App:
    # GTK apps exit when the last window is closed
    CLOSE_ON_LAST_WINDOW = True
    # GTK apps use default command line handling
    HANDLES_COMMAND_LINE = False

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

        # Set any custom styles
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(TOGA_DEFAULT_STYLES)

        context = Gtk.StyleContext()
        context.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_app_commands(self):
        self.interface.commands.add(
            # ---- App menu -----------------------------------
            # Quit should always be the last item, in a section on its own. Invoke
            # `_request_exit` rather than `exit`, because we want to trigger the "OK to
            # exit?" logic.
            Command(
                simple_handler(self.interface._request_exit),
                "Quit " + self.interface.formal_name,
                shortcut=toga.Key.MOD_1 + "q",
                group=Group.APP,
                section=sys.maxsize,
                id=Command.EXIT,
            ),
            # ---- Help menu -----------------------------------
            Command(
                simple_handler(self.interface.about),
                "About " + self.interface.formal_name,
                group=Group.HELP,
                id=Command.ABOUT,
            ),
            Command(
                simple_handler(self.interface.visit_homepage),
                "Visit homepage",
                enabled=self.interface.home_page is not None,
                group=Group.HELP,
                id=Command.VISIT_HOMEPAGE,
            ),
        )

        # If the user has overridden preferences, provide a menu item.
        if overridden(self.interface.preferences):
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.preferences),
                    "Preferences",
                    group=Group.APP,
                    id=Command.PREFERENCES,
                ),
            )  # pragma: no cover

        # If the app has document types, or has overridden new(), provide a menu item.
        # Testbed always has document types, so this must be covered
        if self.interface.document_types:  # pragma: no branch
            known_document_classes = set()
            for i, (extension, document_class) in enumerate(
                self.interface.document_types.items()
            ):
                if document_class not in known_document_classes:
                    self.interface.commands.add(
                        toga.Command(
                            simple_handler(self.interface.new, document_class),
                            text=f"New {document_class.document_type}",
                            shortcut=(
                                (toga.Key.MOD_1 + "n")
                                if not known_document_classes
                                else None
                            ),
                            group=toga.Group.FILE,
                            section=0,
                            order=i,
                            id=Command.NEW.format(extension),
                        ),
                    )
                    known_document_classes.add(document_class)
        elif overridden(self.interface.new):  # pragma: no cover
            # If the user has overridden `new`, provide a menu item. This can't happen
            # in testbed.
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.new),
                    text="New",
                    shortcut=toga.Key.MOD_1 + "n",
                    group=Group.FILE,
                    section=0,
                    order=0,
                    id=Command.NEW.format(None),
                )
            )

        # If the app has document types, or has overridden open(), provide a menu item.
        # Testbed always has document types, so this must be covered
        if self.interface.document_types or overridden(
            self.interface.open
        ):  # pragma: no branch
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface._open),
                    text="Open...",
                    shortcut=toga.Key.MOD_1 + "o",
                    group=Group.FILE,
                    section=0,
                    order=10,
                    id=Command.OPEN,
                ),
            )

        # If the app has document types, or has overridden save(), provide a menu item.
        # Testbed always has document types, so this must be covered
        if self.interface.document_types or overridden(
            self.interface.save
        ):  # pragma: no branch
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.save),
                    text="Save",
                    shortcut=toga.Key.MOD_1 + "s",
                    group=Group.FILE,
                    id=Command.SAVE,
                    section=0,
                    order=20,
                )
            )

        # If the app has document types, or has overridden save_as(), provide a menu item.
        # Testbed always has document types, so this must be covered
        if self.interface.document_types or overridden(
            self.interface.save_as
        ):  # pragma: no branch
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.save_as),
                    text="Save As...",
                    shortcut=toga.Key.MOD_1 + "S",
                    group=Group.FILE,
                    id=Command.SAVE_AS,
                    section=0,
                    order=21,
                )
            )

        # If the app has document types, or has overridden save_all(), provide a menu
        # item. Testbed always has document types, so this must be covered
        if self.interface.document_types or overridden(
            self.interface.save_all
        ):  # pragma: no branch
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.save_all),
                    text="Save All",
                    shortcut=toga.Key.MOD_1 + toga.Key.MOD_2 + "s",
                    group=Group.FILE,
                    id=Command.SAVE_ALL,
                    section=0,
                    order=22,
                )
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
        # Although GTK menus manifest on the Window, they're defined at the
        # application level, and are automatically added to any ApplicationWindow.
        # (or to the top of the screen if the GTK theme requires)

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

    def main_loop(self):
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Retain a reference to the app so that no-window apps can exist
        self.native.hold()

        self.loop.run_forever(application=self.native)

        # Release the reference to the app. This can't be invoked by the testbed,
        # because it's after the `run_forever()` that runs the testbed.
        self.native.release()  # pragma: no cover

    def set_icon(self, icon):
        for window in self.interface.windows:
            window._impl.native.set_icon(icon._impl.native(72))

    def set_main_window(self, window):
        pass

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        display = Gdk.Display.get_default()
        if "WAYLAND_DISPLAY" in os.environ:  # pragma: no-cover-if-linux-x
            # `get_primary_monitor()` doesn't work on wayland, so return as it is.
            return [
                ScreenImpl(native=display.get_monitor(i))
                for i in range(display.get_n_monitors())
            ]
        else:  # pragma: no-cover-if-linux-wayland
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

    def _close_about(self, dialog, **kwargs):
        self.native_about_dialog.destroy()
        self.native_about_dialog = None

    def show_about_dialog(self):
        self.native_about_dialog = Gtk.AboutDialog()
        self.native_about_dialog.set_modal(True)

        icon_impl = toga_App.app.icon._impl
        self.native_about_dialog.set_logo(icon_impl.native(72))

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

    def get_current_window(self):  # pragma: no-cover-if-linux-wayland
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
