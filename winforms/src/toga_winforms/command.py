from System.ComponentModel import InvalidEnumArgumentException

from .keys import toga_to_winforms_key, toga_to_winforms_shortcut
from .libs.wrapper import WeakrefCallable


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []

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
