from rubicon.objc import SEL

from toga_cocoa.keys import cocoa_key
from toga_cocoa.libs import NSMenu, NSMenuItem


def submenu_for_group(group, group_cache):
    """Obtain the submenu representing the command group.

    This will create the submenu if it doesn't exist. It will call itself
    recursively to build the full path to menus inside submenus, returning the
    "leaf" node in the submenu path. Once created, it caches the menu that has been
    created for future lookup.
    """
    try:
        return group_cache[group]
    except KeyError:
        parent_menu = submenu_for_group(group.parent, group_cache)

        menu_item = parent_menu.addItemWithTitle(
            group.text, action=None, keyEquivalent=""
        )
        submenu = NSMenu.alloc().initWithTitle(group.text)
        parent_menu.setSubmenu(submenu, forItem=menu_item)

        # Install the item in the group cache.
        group_cache[group] = submenu
        return submenu


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = set()

    def set_enabled(self, value):
        for item in self.native:
            if isinstance(item, NSMenuItem):
                # Menu item enabled status is determined by the app delegate
                item.menu.update()
            else:
                # Otherwise, assume the native object has
                # and explicit enabled property
                item.setEnabled(value)

    def create_menu_item(self):
        if self.interface.shortcut:
            key, modifier = cocoa_key(self.interface.shortcut)
        else:
            key = ""
            modifier = None

        # Native handlers can be invoked directly as menu actions.
        # Standard wrapped menu items have a `_raw` attribute,
        # and are invoked using the selectMenuItem:
        if hasattr(self.interface.action, "_raw"):
            action = SEL("selectMenuItem:")
        else:
            action = self.interface.action

        item = NSMenuItem.alloc().initWithTitle(
            self.interface.text,
            action=action,
            keyEquivalent=key,
        )

        if modifier is not None:
            item.keyEquivalentModifierMask = modifier

        # Explicit set the initial enabled/disabled state on the menu item
        item.setEnabled(self.interface.enabled)

        # Add the NSMenuItem instance as a native representation of this command.
        self.native.add(item)

        return item
