import sys

from PySide6.QtGui import QAction, QIcon

from toga import Command as StandardCommand, Group, Key

from .keys import toga_to_qt_key


class Command:
    """
    Command `native` property is a list of native widgets associated with the command.

    Native widgets is of type QAction
    """

    def __init__(self, interface):
        self.interface = interface
        self.native = []

    @classmethod
    def standard(self, app, id):
        # ---- File menu ----------
        if id == StandardCommand.PREFERENCES:
            return {
                "text": "Configure " + app.formal_name,
                "shortcut": Key.MOD_1 + Key.SHIFT + ",",
                "group": Group.SETTINGS,
                "section": sys.maxsize - 1,
                "icon": app.icon,
            }
        elif id == StandardCommand.EXIT:
            return {
                "text": "Quit",
                "shortcut": Key.MOD_1 + "q",
                "group": Group.FILE,
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
            return None  # KDE apps have homepage link in about dialog
        elif id == StandardCommand.ABOUT:
            return {
                "text": f"About {app.formal_name}",
                "group": Group.HELP,
                "section": sys.maxsize,
                "icon": app.icon,
            }

        raise ValueError(f"Unknown standard command {id!r}")

    def set_enabled(self, value):
        enabled = self.interface.enabled
        for widget in self.native:
            widget.setEnabled(enabled)

    def qt_click(self):
        self.interface.action()

    def create_menu_item(self):
        item = QAction(self.interface.text)

        if hasattr(self.interface.action, "icon_name"):
            item.setIcon(QIcon.fromTheme(self.interface.action.icon_name))

        if self.interface.text == "Quit":  # Apply the quit icon for application exit.
            item.setIcon(QIcon.fromTheme("application-exit"))

        if self.interface.icon:
            item.setIcon(self.interface.icon._impl.native)

        item.triggered.connect(self.qt_click)

        if self.interface.shortcut is not None:
            item.setShortcut(toga_to_qt_key(self.interface.shortcut))

        item.setEnabled(self.interface.enabled)

        self.native.append(item)

        return item
