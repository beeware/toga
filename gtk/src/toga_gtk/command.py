import sys

from toga import Command as StandardCommand, Group, Key


class Command:
    """Command `native` property is a list of native widgets associated with the
    command.

    Native widgets can be both Gtk.ToolButton and Gio.SimpleAction.
    """

    def __init__(self, interface):
        self.interface = interface
        self.native = []

    @classmethod
    def standard(self, app, id):
        # ---- App menu -----------------------------------
        if id == StandardCommand.PREFERENCES:
            # Preferences should be towards the end of the File menu.
            return {
                "text": "Preferences",
                "group": Group.APP,
                "section": sys.maxsize - 1,
            }
        elif id == StandardCommand.EXIT:
            # Quit should always be the last item, in a section on its own.
            return {
                "text": "Quit",
                "shortcut": Key.MOD_1 + "q",
                "group": Group.APP,
                "section": sys.maxsize,
            }

        # ---- File menu -----------------------------------
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
                "order": 21,
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

    def gtk_activate(self, action, data=None):
        self.interface.action()

    def gtk_clicked(self, action):
        self.interface.action()

    def set_enabled(self, value):
        enabled = self.interface.enabled
        for widget in self.native:
            try:
                widget.set_sensitive(enabled)
            except AttributeError:
                widget.set_enabled(enabled)
