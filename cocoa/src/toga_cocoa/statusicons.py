from rubicon.objc import (
    SEL,
    NSObject,
    NSSize,
    objc_method,
    objc_property,
)

import toga
from toga.command import Group, Separator

from .command import submenu_for_group
from .libs import NSMenu, NSMenuItem, NSSquareStatusItemLength, NSStatusBar


class StatusIcon:
    def __init__(self, interface):
        self.interface = interface
        self.native = None

    def set_icon(self, icon):
        if self.native:
            native_icon = icon._impl.native if icon else toga.App.app.icon._impl.native

            # macOS status icons need to be 22px square, or they render weird
            status_icon = native_icon.copy()
            status_icon.setSize(NSSize(22, 22))
            self.native.button.image = status_icon

    def create(self):
        self.native = NSStatusBar.systemStatusBar.statusItemWithLength(
            NSSquareStatusItemLength
        ).retain()
        self.native.button.toolTip = self.interface.text
        self.set_icon(self.interface.icon)

    def remove(self):
        NSStatusBar.systemStatusBar.removeStatusItem(self.native)
        self.native.release()
        self.native = None


class StatusItemButtonDelegate(NSObject):
    interface = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, sender) -> None:
        self.interface.on_press()


class SimpleStatusIcon(StatusIcon):
    def __init__(self, interface):
        super().__init__(interface)
        self.delegate = StatusItemButtonDelegate.alloc().init()
        self.delegate.interface = interface

    def create(self):
        super().create()
        self.native.button.action = SEL("onPress:")
        self.native.button.target = self.delegate


class MenuStatusIcon(StatusIcon):
    def create(self):
        super().create()
        self.create_menu()

    def create_menu(self):
        submenu = NSMenu.alloc().init()
        self.native.menu = submenu
        return submenu


class StatusIconSet:
    def __init__(self, interface):
        self.interface = interface
        self._menu_items = {}

    def create(self):
        # Menu status icons are the only icons that have extra construction needs.
        # Clear existing menu items
        for menu_item, cmd in self._menu_items.items():
            cmd._impl.remove_menu_item(menu_item)

        # Determine the primary status icon.
        primary_group = self.interface._primary_menu_status_icon
        if primary_group is None:  # pragma: no cover
            # If there isn't at least one menu status icon, then there aren't any menus
            # to populate. This can't happen in the testbed, so it's marked nocover.
            return

        # Recreate the menus for the menu status icons
        group_cache = {
            item: item._impl.create_menu() for item in self.interface._menu_status_icons
        }
        # Map the COMMANDS group to the primary status icon's menu.
        group_cache[Group.COMMANDS] = primary_group._impl.native.menu
        self._menu_items = {}

        for cmd in self.interface.commands:
            try:
                submenu = submenu_for_group(cmd.group, group_cache)
            except ValueError:
                raise ValueError(
                    f"Command {cmd.text!r} does not belong to "
                    "a current status icon group."
                )
            else:
                if isinstance(cmd, Separator):
                    menu_item = NSMenuItem.separatorItem()
                else:
                    menu_item = cmd._impl.create_menu_item()
                    self._menu_items[menu_item] = cmd

                submenu.addItem(menu_item)
