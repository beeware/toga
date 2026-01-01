from rubicon.objc import NSObject, objc_method, objc_property

from toga import Command as StandardCommand

# IMPLEMENTATION NOTES:
# iOS commands are represented differently in different
# contexts, e.g. created directly in the toolbar but using
# a UICommand in the menu bar on iPad.  Therefore, this
# class does not expose the creation of a native object,
# which is handled in the context of each class where
# Commands are used.

# However, places often hook up commands with a target
# and an action.  Thus, an "invoker" class is defined,
# and an instance of it is exposed with each command.
# The "invoker" object should be used to hook up command
# handlers in appropriate locations.


class TogaCommandInvoker(NSObject):
    interface = objc_property(object, weak=True)

    @objc_method
    def executeCommand_(self, sender) -> None:
        self.interface.action()


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []
        self.invoker = TogaCommandInvoker()
        self.invoker.interface = self.interface

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
