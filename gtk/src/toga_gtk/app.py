import asyncio
import signal
import sys
from pathlib import Path

import gbulb

import toga
from toga import App as toga_App
from toga.command import Command, Separator

from .keys import gtk_accel
from .libs import TOGA_DEFAULT_STYLES, AppIndicator, Gdk, Gio, GLib, Gtk
from .window import Window


class MainWindow(Window):
    def create(self):
        self.native = Gtk.ApplicationWindow()
        self.native.set_role("MainWindow")
        icon_impl = toga_App.app.icon._impl
        self.native.set_icon(icon_impl.native_72)

    def gtk_delete_event(self, *args):
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
        # Activate is a no-op, but GTK complains if you don't implement it.
        self.native.connect("activate", self.gtk_activate)

        self.actions = None

    def gtk_startup(self, data=None):
        # As the call to _startup() isn't made in the constructor, the on_change
        # handler for commands is already installed. We don't want to start creating
        # menus until after _startup() and any default app commands have been created,
        # so suspend updates; this will call create_menus when the context exits.
        with self.interface.commands.suspend_updates():
            self.interface._startup()

            self.create_app_commands()

        # Set any custom styles
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(TOGA_DEFAULT_STYLES)

        context = Gtk.StyleContext()
        context.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def create_app_commands(self):
        # Set up the default commands for the interface.
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

        # The first status item group in a windowless app (by group ordering)
        # gets the app control commands. The app control commands always form
        # the last 2 sections in the group.
        try:
            main_status_item = sorted(
                {
                    item.group
                    for item in self.interface.commands
                    if not isinstance(item, Separator) and item.group.is_status_item
                }
            )[0]
        except IndexError:
            pass
        else:
            self.interface.commands.add(
                Command(
                    self._menu_about,
                    "About " + self.interface.formal_name,
                    group=main_status_item,
                    section=sys.maxsize - 1,
                ),
                Command(
                    None,
                    "Preferences",
                    group=main_status_item,
                    section=sys.maxsize - 1,
                ),
                # Quit should always be the last item, in a section on its own
                Command(
                    self._menu_quit,
                    "Quit " + self.interface.formal_name,
                    shortcut=toga.Key.MOD_1 + "q",
                    group=main_status_item,
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
        self._menu_items = {}
        self._menu_groups = {}
        self._status_indicators = {}

        # Hide all the status indicators. They will be made visible
        # again if the status item group still exists.
        for _, indicator in self._status_indicators:
            indicator.set_status(AppIndicator.IndicatorStatus.PASSIVE)

        # Create the menu for the top level menubar.
        menubar = Gio.Menu()
        section = None
        for cmd in self.interface.commands:
            submenu, created = self._submenu(cmd.group, menubar)
            if isinstance(cmd, Separator):
                section = None
                # Gtk.Menu (used by status items) uses an explicit separator item.
                if isinstance(submenu, Gtk.Menu):
                    item = Gtk.SeparatorMenuItem.new()
                    submenu.append(item)
                    submenu.show_all()
            else:
                # Status items use Gtk.Menu; regular menus use Gio.Menu
                if isinstance(submenu, Gtk.Menu):
                    item = Gtk.MenuItem.new_with_label(cmd.text)
                    item.connect("activate", cmd._impl.gtk_activate)
                    submenu.append(item)
                    submenu.show_all()
                else:
                    if created:
                        section = None

                    if section is None:
                        section = Gio.Menu()
                        submenu.append_section(None, section)

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
        #
        # This is required because of inconsistencies in how the Gnome
        # shell operates on different windowing environments;
        # see #872 for details.
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-shell-shows-menubar", False)

    def _submenu(self, group, menubar):
        try:
            return self._menu_groups[group], False
        except KeyError:
            if group is None:
                submenu = menubar
            elif group.is_status_item:
                if AppIndicator is None:
                    raise RuntimeError(
                        "Unable to import AyatanaAppIndicator3. Ensure that "
                        "the system package providing AyatanaAppIndicator3 "
                        "its GTK bindings have been installed."
                    )

                try:
                    # Indicators must be unique; so make sure the indicator is
                    # re-used if the group has already been used to create an
                    # indicator.
                    indicator = self._status_indicators[group]
                except KeyError:
                    indicator = AppIndicator.Indicator.new(
                        f"indicator-{id(group)}",
                        "",
                        AppIndicator.IndicatorCategory.APPLICATION_STATUS,
                    )
                    self._status_indicators[group] = indicator

                icon = group.icon._impl if group.icon else self.interface.icon._impl

                indicator.set_title(group.text)
                indicator.set_icon_full(str(icon.paths[32]), group.text)
                indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)

                submenu = Gtk.Menu.new()
                indicator.set_menu(submenu)
            else:
                parent_menu, _ = self._submenu(group.parent, menubar)
                text = group.text
                if text == "*":
                    text = self.interface.formal_name

                # GTK has 2 types of menu - GTK.Menu (used for status icons),
                # and Gio.Menu (used for normal app menus).
                if isinstance(parent_menu, Gtk.Menu):
                    submenu = Gtk.Menu.new()
                    item = Gtk.MenuItem.new_with_label(text)
                    item.set_submenu(submenu)

                    parent_menu.append(item)
                    parent_menu.show_all()
                else:
                    submenu = Gio.Menu()
                    parent_menu.append_submenu(text, submenu)

            # Install the item in the group cache.
            self._menu_groups[group] = submenu

            return submenu, True

    def main_loop(self):
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Retain a reference to the app so that no-window apps can exist
        self.native.hold()

        # Run the event loop.
        self.loop.run_forever(application=self.native)

        # Release the reference to the app
        self.native.release()

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        self.native_about_dialog = Gtk.AboutDialog()
        self.native_about_dialog.set_modal(True)

        icon_impl = toga_App.app.icon._impl
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

    def _close_about(self, dialog, *args):
        self.native_about_dialog.destroy()
        self.native_about_dialog = None

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


class SimpleApp(App):
    def create_app_commands(self):
        pass

    def create_menus(self):
        pass


class WindowlessApp(App):
    pass


class DocumentApp(App):  # pragma: no cover
    def create_app_commands(self):
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
