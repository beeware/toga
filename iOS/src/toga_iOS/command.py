from toga import Command as StandardCommand


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []

    @classmethod
    def standard(cls, app, id):
        if id in {
            StandardCommand.ABOUT,
            StandardCommand.EXIT,
            StandardCommand.NEW,
            StandardCommand.OPEN,
            StandardCommand.PREFERENCES,
            StandardCommand.SAVE,
            StandardCommand.SAVE_AS,
            StandardCommand.SAVE_ALL,
            StandardCommand.VISIT_HOMEPAGE,
        }:
            # These are valid commands, but they're not defined on iOS.
            return None

        raise ValueError(f"Unknown standard command {id!r}")

    def set_enabled(self, value):
        pass
