import System.Windows.Forms as WinForms

import toga
from toga.command import Separator

from .libs.wrapper import WeakrefCallable


class BaseStatusIcon:
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
        self.set_icon(self.interface.icon)

    def remove(self):
        self.native.Visible = False
        self.native.Dispose()


class StatusIcon(BaseStatusIcon):
    def create(self):
        super().create()
        self.native.Click += WeakrefCallable(self.winforms_click)

    def winforms_click(self, sender, event):
        self.interface.on_press()


class MenuStatusIcon(BaseStatusIcon):
    def _submenu(self, group, group_cache):
        try:
            return group_cache[group]
        except KeyError:
            if group.parent is None:
                submenu = self.native.ContextMenu
            else:
                parent_menu = self._submenu(group.parent, group_cache)

                submenu = WinForms.MenuItem(group.text)

                parent_menu.MenuItems.Add(submenu)

            group_cache[group] = submenu
        return submenu

    def create_menus(self):
        # Clear existing items
        submenu = WinForms.ContextMenu()
        self.native.ContextMenu = submenu

        # Create a clean menubar instance.
        group_cache = {}
        for cmd in self.interface.commands:
            submenu = self._submenu(cmd.group, group_cache)
            if isinstance(cmd, Separator):
                menu_item = "-"
            else:
                menu_item = cmd._impl.create_menu_item(WinForms.MenuItem)

            submenu.MenuItems.Add(menu_item)
