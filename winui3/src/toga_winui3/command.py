import sys

from toga import Command as StandardCommand, Group, Key

from .libs.nativeevents import events_handled


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = {}

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

    def native_event_Click(self, sender, args):
        return self.interface.action()

    def set_enabled(self, value):
        is_enabled = self.interface.enabled
        for item in self.native.values():
            item.IsEnabled = is_enabled

    def create_menu_item(self, window_id, NativeClass):
        item = events_handled(NativeClass)
        item.Text = self.interface.text
        item.event_handler.Click += self.native_event_Click

        if self.interface.shortcut is not None:
            self.interface.factory.not_implemented("Command shortcuts")

        item.IsEnabled = self.interface.enabled

        self.native[window_id] = item

        return item
