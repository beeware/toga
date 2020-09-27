import toga

from .keys import cocoa_key

from .libs import SEL, NSMenu, NSMenuItem


class MenuBuilder:

    def __init__(self, commands_set):
        self.commands_set = commands_set

    def build(self):
        menubar = NSMenu.alloc().initWithTitle('MainMenu')
        submenu = None
        menuItem = None
        for cmd in self.commands_set:
            if cmd == toga.GROUP_BREAK:
                menubar.setSubmenu(submenu, forItem=menuItem)
                submenu = None
            elif cmd == toga.SECTION_BREAK:
                submenu.addItem_(NSMenuItem.separatorItem())
            else:
                if submenu is None:
                    menuItem = menubar.addItemWithTitle(cmd.group.label, action=None,
                                                        keyEquivalent='')
                    submenu = NSMenu.alloc().initWithTitle(cmd.group.label)
                    submenu.setAutoenablesItems(False)

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

        if submenu:
            menubar.setSubmenu(submenu, forItem=menuItem)
        return menubar
