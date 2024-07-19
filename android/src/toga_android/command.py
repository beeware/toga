import sys

from org.beeware.android import MainActivity

from toga import Command as StandardCommand


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []

    @classmethod
    def standard(cls, app, id):
        # ---- Help menu ----------------------------------
        if id == StandardCommand.ABOUT:
            return {
                "text": f"About {app.formal_name}",
                "section": sys.maxsize,
            }
        # ---- Undefined commands--------------------------
        elif id in {
            StandardCommand.EXIT,
            StandardCommand.OPEN,
            StandardCommand.PREFERENCES,
            StandardCommand.VISIT_HOMEPAGE,
        }:
            # These are valid commands, but they're not defined on Android.
            return None

        raise ValueError(f"Unknown standard command {id!r}")

    def set_enabled(self, value):
        MainActivity.singletonThis.invalidateOptionsMenu()
