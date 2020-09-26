from .keys import toga_to_winforms_key
from .libs import WinForms
import toga


class MenuBuilder:

    def __init__(self, commands_set):
        self.commands_set = commands_set

    def build(self):
        menubar = WinForms.MenuStrip()
        submenu = None
        for cmd in self.commands_set:
            if cmd == toga.GROUP_BREAK:
                menubar.Items.Add(submenu)
                submenu = None
            elif cmd == toga.SECTION_BREAK:
                submenu.DropDownItems.Add('-')
            else:
                if submenu is None:
                    submenu = WinForms.ToolStripMenuItem(cmd.group.label)
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
