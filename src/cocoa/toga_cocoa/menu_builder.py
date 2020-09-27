import toga

from .keys import cocoa_key

from .libs import SEL, NSMenu, NSMenuItem


class MenuBuilder:

    def __init__(self, commands_set):
        self.commands_set = commands_set
        self.group_menus = {}

    def build(self):
        menubar = NSMenu.alloc().initWithTitle('MainMenu')
        submenu = None
        for cmd in self.commands_set:
            if cmd == toga.GROUP_BREAK:
                submenu = None
            elif cmd == toga.SECTION_BREAK:
                submenu.addItem_(NSMenuItem.separatorItem())
            else:
                if submenu is None:
                    submenu = self.get_or_create_group_menu(cmd.group, menubar)
                if cmd.shortcut:
                    key, modifier = cocoa_key(cmd.shortcut)
                else:
                    key = ''
                    modifier = None

                item = NSMenuItem.alloc().initWithTitle(
                    cmd.label,
                    action=SEL('selectMenuItem:'),
                    keyEquivalent=key,
                )
                if modifier is not None:
                    item.keyEquivalentModifierMask = modifier

                cmd._impl.native.append(item)

                # This line may appear redundant, but it triggers the logic
                # to force the enabled status on the underlying widgets.
                cmd.enabled = cmd.enabled
                submenu.addItem(item)
        return menubar

    def get_or_create_group_menu(self, group, menubar):
        if group is None:
            return menubar
        if group.label in self.group_menus:
            return self.group_menus[group.label]
        parent_menu = self.get_or_create_group_menu(group.parent, menubar)
        menu_item = parent_menu.addItemWithTitle(
            group.label, action=None, keyEquivalent=''
        )
        submenu = NSMenu.alloc().initWithTitle(group.label)
        submenu.setAutoenablesItems(False)
        parent_menu.setSubmenu(submenu, forItem=menu_item)
        self.group_menus[group.label] = submenu
        return submenu
