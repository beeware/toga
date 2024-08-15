import toga
from toga.command import Separator

from .libs import AppIndicator, Gtk


class BaseStatusIcon:
    def __init__(self, interface):
        self.interface = interface
        self.native = None

    def set_icon(self, icon):
        if self.native:
            path = str(
                icon._impl.paths[32] if icon else toga.App.app.icon._impl.paths[32]
            )
            self.native.set_icon_full(path, "")

    def create(self):
        if AppIndicator is None:
            raise RuntimeError(
                "Unable to import AyatanaAppIndicator3. Ensure that "
                "the system package providing AyatanaAppIndicator3 "
                "its GTK bindings have been installed."
            )

        self.native = AppIndicator.Indicator.new(
            f"indicator-{id(self)}",
            "",
            AppIndicator.IndicatorCategory.APPLICATION_STATUS,
        )
        self.native.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.set_icon(self.interface.icon)

    def remove(self):
        self.native.set_status(AppIndicator.IndicatorStatus.PASSIVE)


class StatusIcon(BaseStatusIcon):
    def create(self):
        super().create()
        # FIXME: Need to work out how to display an icon-only status item,
        # and connect the activate event to self.interface.on_press()


class MenuStatusIcon(BaseStatusIcon):
    def _submenu(self, group, group_cache):
        try:
            return group_cache[group]
        except KeyError:
            if group.parent is None:
                submenu = self.native.get_menu()
            else:
                parent_menu = self._submenu(group.parent, group_cache)

                submenu = Gtk.Menu.new()
                item = Gtk.MenuItem.new_with_label(group.text)
                item.set_submenu(submenu)

                parent_menu.append(item)
                parent_menu.show_all()

            group_cache[group] = submenu
        return submenu

    def create_menus(self):
        # Clear existing menu
        submenu = Gtk.Menu.new()
        self.native.set_menu(submenu)

        # Create a clean menubar instance.
        group_cache = {}
        for cmd in self.interface.commands:
            submenu = self._submenu(cmd.group, group_cache)

            if isinstance(cmd, Separator):
                menu_item = Gtk.SeparatorMenuItem.new()
            else:
                menu_item = Gtk.MenuItem.new_with_label(cmd.text)
                menu_item.connect("activate", cmd._impl.gtk_activate)

            submenu.append(menu_item)
            submenu.show_all()
