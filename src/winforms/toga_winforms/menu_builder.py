from .keys import toga_to_winforms_key
from .libs import WinForms
import toga


class MenuBuilder:

    def __init__(self, commands_set):
        self.commands_set = commands_set
        self.group_menus = {}

    def build(self):
        menubar = WinForms.MenuStrip()
        group = None
        submenu = None
        for cmd in self.commands_set:
            if cmd == toga.GROUP_BREAK:
                if group.parent is None:
                    menubar.Items.Add(submenu)
                else:
                    self.get_or_create_group_menu(group.parent).DropDownItems.Add(
                        submenu
                    )
                submenu = None
                group = None
            elif cmd == toga.SECTION_BREAK:
                submenu.DropDownItems.Add('-')
            else:
                if submenu is None:
                    group = cmd.group
                    submenu = self.get_or_create_group_menu(group)
                item = WinForms.ToolStripMenuItem(cmd.label)
                if cmd.action:
                    item.Click += cmd._impl.as_handler()
                item.Enabled = cmd.enabled
                if cmd.shortcut is not None:
                    shortcut_keys = toga_to_winforms_key(cmd.shortcut)
                    item.ShortcutKeys = shortcut_keys
                    item.ShowShortcutKeys = True
                cmd._impl.native.append(item)
                submenu.DropDownItems.Add(item)
        if submenu:
            menubar.Items.Add(submenu)
        return menubar

    def get_or_create_group_menu(self, group):
        if group.label in self.group_menus:
            return self.group_menus[group.label]
        submenu = WinForms.ToolStripMenuItem(group.label)
        self.group_menus[group.label] = submenu
        return submenu
