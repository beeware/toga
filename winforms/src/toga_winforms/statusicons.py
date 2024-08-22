import System.Windows.Forms as WinForms

import toga
from toga.command import Group, Separator

from .libs.wrapper import WeakrefCallable


class StatusIcon:
    def __init__(self, interface):
        self.interface = interface
        self.native = None

    def set_icon(self, icon):
        if self.native:
            self.native.Icon = (
                icon._impl.native if icon else toga.App.app.icon._impl.native
            )

    def create(self):
        self.native = WinForms.NotifyIcon()
        self.native.Visible = True
        self.native.Text = self.interface.text
        self.set_icon(self.interface.icon)

    def remove(self):
        self.native.Visible = False
        self.native.Dispose()
        self.native = None


class SimpleStatusIcon(StatusIcon):
    def create(self):
        super().create()
        self.native.Click += WeakrefCallable(self.winforms_click)

    def winforms_click(self, sender, event):
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

                submenu = WinForms.MenuItem(group.text)

                parent_menu.MenuItems.Add(submenu)

            group_cache[group] = submenu
        return submenu

    def create(self):
        # Menu status icons are the only icons that have extra construction needs.
        # Clear existing menus
        for item in self.interface._menu_status_icons:
            submenu = WinForms.ContextMenu()
            item._impl.native.ContextMenu = submenu

        # Determine the primary status icon.
        primary_group = self.interface._primary_menu_status_icon
        if primary_group is None:  # pragma: no cover
            # If there isn't at least one menu status icon, then there aren't any menus
            # to populate. This can't be replicated in the testbed.
            return

        # Add the menu status items to the cache
        group_cache = {
            item: item._impl.native.ContextMenu
            for item in self.interface._menu_status_icons
        }
        # Map the COMMANDS group to the primary status icon's menu.
        group_cache[Group.COMMANDS] = primary_group._impl.native.ContextMenu
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
                    menu_item = "-"
                else:
                    menu_item = cmd._impl.create_menu_item(WinForms.MenuItem)

                submenu.MenuItems.Add(menu_item)
