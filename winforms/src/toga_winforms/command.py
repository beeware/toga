import sys

from System.ComponentModel import InvalidEnumArgumentException

from toga import Command as StandardCommand, Group, Key
from toga_winforms.keys import toga_to_winforms_key, toga_to_winforms_shortcut
from toga_winforms.libs.wrapper import WeakrefCallable


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []

    @classmethod
    def standard(self, app, id):
        # ---- File menu -----------------------------------
        if id == StandardCommand.NEW:
            return {
                "text": "New",
                "shortcut": Key.MOD_1 + "n",
                "group": Group.FILE,
                "section": 0,
                "order": 0,
            }
        elif id == StandardCommand.OPEN:
            return {
                "text": "Open...",
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
                "section": 0,
                "order": 20,
            }
        elif id == StandardCommand.SAVE_AS:
            return {
                "text": "Save As...",
                "shortcut": Key.MOD_1 + "S",
                "group": Group.FILE,
                "section": 0,
                "order": 21,
            }
        elif id == StandardCommand.SAVE_ALL:
            return {
                "text": "Save All",
                "shortcut": Key.MOD_1 + Key.MOD_2 + "s",
                "group": Group.FILE,
                "section": 0,
                "order": 22,
            }
        elif id == StandardCommand.PREFERENCES:
            # Preferences should be towards the end of the File menu.
            return {
                "text": "Preferences",
                "group": Group.FILE,
                "section": sys.maxsize - 1,
            }
        elif id == StandardCommand.EXIT:
            # Quit should always be the last item, in a section on its own.
            return {
                "text": "Exit",
                "group": Group.FILE,
                "section": sys.maxsize,
            }
        # ---- Help menu -----------------------------------
        elif id == StandardCommand.VISIT_HOMEPAGE:
            return {
                "text": "Visit homepage",
                "enabled": app.home_page is not None,
                "group": Group.HELP,
            }
        elif id == StandardCommand.ABOUT:
            return {
                "text": f"About {app.formal_name}",
                "group": Group.HELP,
                "section": sys.maxsize,
            }

        raise ValueError(f"Unknown standard command {id!r}")

    def winforms_Click(self, sender, event):
        return self.interface.action()

    def set_enabled(self, value):
        if self.native:
            for widget in self.native:
                widget.Enabled = self.interface.enabled

    def create_menu_item(self, WinformsClass):
        item = WinformsClass(self.interface.text)

        item.Click += WeakrefCallable(self.winforms_Click)
        if self.interface.shortcut is not None:
            try:
                item.ShortcutKeys = toga_to_winforms_key(self.interface.shortcut)
                # The Winforms key enum is... daft. The "oem" key
                # values render as "Oem" or "Oemcomma", so we need to
                # *manually* set the display text for the key shortcut.
                item.ShortcutKeyDisplayString = toga_to_winforms_shortcut(
                    self.interface.shortcut
                )
            except (
                ValueError,
                InvalidEnumArgumentException,
            ) as e:  # pragma: no cover
                # Make this a non-fatal warning, because different backends may
                # accept different shortcuts.
                print(f"WARNING: invalid shortcut {self.interface.shortcut!r}: {e}")

        item.Enabled = self.interface.enabled

        self.native.append(item)

        return item
