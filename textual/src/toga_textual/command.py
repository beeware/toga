from toga import Command as StandardCommand


class Command:
    """Command `native` property is a list of native widgets associated with the
    command."""

    def __init__(self, interface):
        self.interface = interface
        self.native = []

    @classmethod
    def standard(cls, app, id):
        # ---- Non-existent commands ----------------------------------
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
            # These commands are valid, but don't exist on textual.
            return None

        raise ValueError(f"Unknown standard command {id!r}")

    def set_enabled(self, value):
        pass
