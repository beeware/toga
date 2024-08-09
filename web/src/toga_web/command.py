from toga import Command as StandardCommand, Group


class Command:
    """Command `native` property is a list of native widgets associated with the
    command."""

    def __init__(self, interface):
        self.interface = interface
        self.native = []

    @classmethod
    def standard(cls, app, id):
        # ---- Help menu ----------------------------------
        if id == StandardCommand.ABOUT:
            return {
                "text": f"About {app.formal_name}",
                "group": Group.HELP,
            }
        elif id == StandardCommand.PREFERENCES:
            return {
                "text": "Preferences",
                "group": Group.HELP,
            }
        # ---- Non-existent commands ----------------------------------
        elif id in {
            StandardCommand.EXIT,
            StandardCommand.NEW,
            StandardCommand.OPEN,
            StandardCommand.SAVE,
            StandardCommand.SAVE_AS,
            StandardCommand.SAVE_ALL,
            StandardCommand.VISIT_HOMEPAGE,
        }:
            # These commands are valid, but don't exist on web.
            return None

        raise ValueError(f"Unknown standard command {id!r}")

    def dom_click(self, event):
        self.interface.action()

    def set_enabled(self, value):
        pass
        # enabled = self.interface.enabled
        # for widget in self.native:
        #     try:
        #         widget.set_sensitive(enabled)
        #     except AttributeError:
        #         widget.set_enabled(enabled)
