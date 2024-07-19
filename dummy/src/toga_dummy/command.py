import sys

from toga import Command as StandardCommand, Group
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
        elif id == StandardCommand.OPEN:
            return {
                "text": "Open",
                "group": Group.FILE,
                "section": 0,
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
