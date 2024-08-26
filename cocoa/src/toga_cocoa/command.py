import sys

from toga import Command as StandardCommand, Group, Key
from toga_cocoa.libs import NSMenuItem


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = set()

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
