from toga import Command as StandardCommand


class Command:
    """Command `native` property is a list of native widgets associated with the
    command."""

    def __init__(self, interface):
        self.interface = interface
        self.native = []

    @classmethod
    def standard(cls, app, id):
        if id == StandardCommand.PREFERENCES:
            return None
        elif id == StandardCommand.EXIT:
            return None
        elif id == StandardCommand.OPEN:
            return None
        elif id == StandardCommand.ABOUT:
            return None
        elif id == StandardCommand.VISIT_HOMEPAGE:
            return None

        raise ValueError(f"Unknown standard command {id!r}")

    def set_enabled(self, value):
        pass
