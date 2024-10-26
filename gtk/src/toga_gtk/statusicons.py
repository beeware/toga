import toga
from toga.command import Group, Separator

from .libs import Gtk, XApp


class StatusIcon:
    def __init__(self, interface):
        self.interface = interface
        self.native = None

    def set_icon(self, icon):
        if self.native:
            path = str(
                icon._impl.paths[32] if icon else toga.App.app.icon._impl.paths[32]
            )
            self.native.set_icon_name(path)

    def create(self):
        if XApp is None:  # pragma: no cover
            # Can't replicate this in testbed
            raise RuntimeError(
                "Unable to import XApp. Ensure that the system package "
                "providing libxapp and its GTK bindings have been installed."
            )

        self.native = XApp.StatusIcon.new()
        self.native.set_tooltip_text(self.interface.text)
        self.set_icon(self.interface.icon)

    def remove(self):
        del self.native
        self.native = None


class SimpleStatusIcon(StatusIcon):
    def create(self):
        super().create()
        self.native.connect("activate", self.gtk_activate)

    def gtk_activate(self, icon, button, time):
        self.interface.on_press()


class MenuStatusIcon(StatusIcon):
    pass


class StatusIconSet:
    def __init__(self, interface):
        self.interface = interface
        self._menu_items = {}

    def _submenu(self, group, group_cache):
        try:
            return group_cache[group]
        except KeyError:
            if group is None:
                raise ValueError("Unknown top level item")
            else:
                parent_menu = self._submenu(group.parent, group_cache)

                submenu = Gtk.Menu.new()
                item = Gtk.MenuItem.new_with_label(group.text)
                item.set_submenu(submenu)

                parent_menu.append(item)
                parent_menu.show_all()

            group_cache[group] = submenu
        return submenu

    def create(self):
        # Menu status icons are the only icons that have extra construction needs.
        # Clear existing menus
        for item in self.interface._menu_status_icons:
            submenu = Gtk.Menu.new()
            item._impl.native.set_primary_menu(submenu)

        # Determine the primary status icon.
        primary_group = self.interface._primary_menu_status_icon
        if primary_group is None:  # pragma: no cover
            # If there isn't at least one menu status icon, then there aren't any menus
            # to populate. This can't be replicated in the testbed.
            return

        # Add the menu status items to the cache
        group_cache = {
            item: item._impl.native.get_primary_menu()
            for item in self.interface._menu_status_icons
        }
        # Map the COMMANDS group to the primary status icon's menu.
        group_cache[Group.COMMANDS] = primary_group._impl.native.get_primary_menu()
        self._menu_items = {}

        for cmd in self.interface.commands:
            try:
                submenu = self._submenu(cmd.group, group_cache)
            except ValueError:
                raise ValueError(
                    f"Command {cmd.text!r} does not belong to "
                    "a current status icon group."
                )
            else:
                if isinstance(cmd, Separator):
                    menu_item = Gtk.SeparatorMenuItem.new()
                else:
                    menu_item = Gtk.MenuItem.new_with_label(cmd.text)
                    menu_item.connect("activate", cmd._impl.gtk_activate)

                submenu.append(menu_item)
                submenu.show_all()
