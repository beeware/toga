import sys

from rubicon.objc import SEL

from toga import Command as StandardCommand, Group, Key
from toga_cocoa.keys import cocoa_key
from toga_cocoa.libs import NSMenu, NSMenuItem


def submenu_for_group(group, group_cache):
    """Obtain the submenu representing the command group.

    This will create the submenu if it doesn't exist. It will call itself recursively to
    build the full path to menus inside submenus, returning the "leaf" node in the
    submenu path. Once created, it caches the menu that has been created for future
    lookup.

    This method assumes that the top-level item (for group=None) exists in the
    group_cache. If it doesn't, a ValueError is raised when the top level group is
    requested.

    :param group: The group to turn into a submenu.
    :param group_cache: The cache of existing groups.
    :raises ValueError: If the top level group cannot be found in the group cache.
    """
    try:
        return group_cache[group]
    except KeyError:
        if group is None:
            raise ValueError("Cannot find top level group")
        else:
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
    menu_items = {}

    def __init__(self, interface):
        self.interface = interface
        self.native = set()

    @classmethod
    def for_menu_item(cls, item):
        return cls.menu_items[item]

    @classmethod
    def standard(cls, app, id):
        # ---- App menu -----------------------------------
        if id == StandardCommand.ABOUT:
            # About should be the first menu item
            return {
                "text": f"About {app.formal_name}",
                "group": Group.APP,
                "section": -1,
            }
        elif id == StandardCommand.PREFERENCES:
            return {
                "text": "Settings\u2026",
                "shortcut": Key.MOD_1 + ",",
                "group": Group.APP,
                "section": 20,
            }
        elif id == StandardCommand.EXIT:
            # Quit should always be the last item, in a section on its own.
            return {
                "text": f"Quit {app.formal_name}",
                "shortcut": Key.MOD_1 + "q",
                "group": Group.APP,
                "section": sys.maxsize,
            }
        # ---- File menu ----------------------------------
        elif id == StandardCommand.NEW:
            return {
                "text": "New",
                "shortcut": Key.MOD_1 + "n",
                "group": Group.FILE,
                "section": 0,
                "order": 0,
            }
        elif id == StandardCommand.OPEN:
            return {
                "text": "Open\u2026",
                "shortcut": Key.MOD_1 + "o",
                "group": Group.FILE,
                "section": 0,
                "order": 10,
            }
        elif id == StandardCommand.SAVE:
            return {
                "text": "Save",
                "shortcut": Key.MOD_1 + "s",
                "group": Group.FILE,
                "section": 30,
                "order": 10,
            }
        elif id == StandardCommand.SAVE_AS:
            return {
                "text": "Save As\u2026",
                "shortcut": Key.MOD_1 + "S",
                "group": Group.FILE,
                "section": 30,
                "order": 11,
            }
        elif id == StandardCommand.SAVE_ALL:
            return {
                "text": "Save All",
                "shortcut": Key.MOD_1 + Key.MOD_2 + "s",
                "group": Group.FILE,
                "section": 30,
                "order": 12,
            }
        # ---- Help menu ----------------------------------
        elif id == StandardCommand.VISIT_HOMEPAGE:
            return {
                "text": "Visit homepage",
                "enabled": app.home_page is not None,
                "group": Group.HELP,
            }

        raise ValueError(f"Unknown standard command {id!r}")

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

        # Add the menu item instance to the instance map.
        self.menu_items[item] = self.interface

        return item

    def remove_menu_item(self, menu_item):
        menu_item.menu.removeItem(menu_item)
        self.native.remove(menu_item)
        self.menu_items.pop(menu_item)
