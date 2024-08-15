from rubicon.objc import (
    SEL,
    NSObject,
    NSSize,
    objc_method,
    objc_property,
)

import toga
from toga.command import Separator

from .command import submenu_for_group
from .libs import NSMenu, NSMenuItem, NSSquareStatusItemLength, NSStatusBar


class BaseStatusIcon:
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
        )
        self.set_icon(self.interface.icon)

    def clear_menus(self):
        pass

    def remove(self):
        NSStatusBar.systemStatusBar.removeStatusItem(self.native)


class StatusItemButtonDelegate(NSObject):
    interface = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, sender) -> None:
        self.interface.on_press()


class StatusIcon(BaseStatusIcon):
    def __init__(self, interface):
        super().__init__(interface)
        self.delegate = StatusItemButtonDelegate.alloc().init()
        self.delegate.interface = interface

    def create(self):
        super().create()
        self.native.button.action = SEL("onPress:")
        self.native.button.target = self.delegate


class MenuStatusIcon(BaseStatusIcon):
    def create(self):
        super().create()
        self._menu_items = {}
        submenu = NSMenu.alloc().init()
        self.native.menu = submenu

    def create_menus(self):
        # Clear existing items
        for menu_item, cmd in self._menu_items.items():
            cmd._impl.remove_menu_item(menu_item)

        # Create a clean menubar instance.
        group_cache = {}
        self._menu_items = {}

        for cmd in self.interface.commands:
            submenu = submenu_for_group(
                cmd.group,
                group_cache,
                default_parent=self.native.menu,
            )

            if isinstance(cmd, Separator):
                menu_item = NSMenuItem.separatorItem()
            else:
                menu_item = cmd._impl.create_menu_item()
                self._menu_items[menu_item] = cmd

            submenu.addItem(menu_item)
