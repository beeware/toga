import sys

from toga import Command as StandardCommand, Group, Key
from toga_dummy.utils import LoggedObject


class Command(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    @classmethod
    def standard(cls, app, id):
        # ---- File menu -----------------------------------
        if id == StandardCommand.PREFERENCES:
            return {
                "text": "Preferences",
                "group": Group.APP,
            }
        elif id == StandardCommand.EXIT:
            # Quit should always be the last item, in a section on its own.
            return {
                "text": "Exit",
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
                "text": "Open",
                "group": Group.FILE,
                "section": 0,
                "order": 10,
            }
        elif id == StandardCommand.SAVE:
            return {
                "text": "Save",
                "group": Group.FILE,
                "section": 10,
                "order": 0,
            }
        elif id == StandardCommand.SAVE_AS:
            return {
                "text": "Save As",
                "group": Group.FILE,
                "section": 10,
                "order": 1,
            }
        elif id == StandardCommand.SAVE_ALL:
            return {
                "text": "Save All",
                "group": Group.FILE,
                "section": 10,
                "order": 2,
            }
        # ---- Help menu ----------------------------------
        elif id == StandardCommand.ABOUT:
            return {
                "text": f"About {app.formal_name}",
                "group": Group.HELP,
            }
        elif id == StandardCommand.VISIT_HOMEPAGE:
            # Dummy doesn't have a visit homepage menu item.
            # This lets us verify the "platform doesn't support command"
            # logic.
            return None

        raise ValueError(f"Unknown standard command {id!r}")

    def set_enabled(self, value):
        self._action("set enabled", value=value)
