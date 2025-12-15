from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from toga.command import Group, Separator

# Not implemented on Qt yet.


class StatusIcon:
    def __init__(self, interface):
        self.interface = interface
        self.native = None

    def set_icon(self, icon):
        if self.native is None:
            return
        if icon is not None:
            self.native.setIcon(icon._impl.native)
        else:
            self.native.setIcon(QIcon())
            self.interface.factory.not_implemented("StatusIcon with only text")

    def create(self):
        self.native = QSystemTrayIcon()
        self.native.setToolTip(self.interface.text)
        self.set_icon(self.interface.icon)
        self.native.show()

    # Remove no-cover when this is implemented
    def remove(self):
        if self.native:
            self.native.hide()
            self.native.deleteLater()

        self.native = None


class SimpleStatusIcon(StatusIcon):
    def create(self):
        super().create()
        self.native.activated.connect(self.qt_on_activated)

    def qt_on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # pragma: no branch
            self.interface.on_press()


class MenuStatusIcon(StatusIcon):
    def create(self):
        super().create()
        self.create_menu()

    def create_menu(self):
        self.submenu = QMenu(self.interface.text)
        self.native.setContextMenu(self.submenu)


class StatusIconSet:
    def __init__(self, interface):
        self.interface = interface
        self._menu_items = {}

    def _submenu(self, group, group_cache):
        try:
            return group_cache[group]
        except KeyError as exc:
            if group is None:
                raise ValueError("Unknown top level item") from exc
            else:
                parent_menu = self._submenu(group.parent, group_cache)
                submenu = parent_menu.addMenu(group.text)
            group_cache[group] = submenu
        return submenu

    def create(self):
        """Create the status icons.

        This gets called on App creation, and then on any changes to the status icon
        command set.
        """
        # Menu status icons are the only icons that have extra construction needs.
        # Clear existing menu items
        for item in self.interface._menu_status_icons:
            submenu = item._impl.create_menu()

        # Determine the primary status icon.
        primary_group = self.interface._primary_menu_status_icon
        if primary_group is None:  # pragma: no cover
            # If there isn't at least one menu status icon, then there aren't any menus
            # to populate. This can't happen in the testbed, so it's marked nocover.
            return

        # Add the menu status items to the cache
        group_cache = {
            item: item._impl.native.contextMenu()
            for item in self.interface._menu_status_icons
        }
        # Map the COMMANDS group to the primary status icon's menu.
        group_cache[Group.COMMANDS] = primary_group._impl.native.contextMenu()
        self._menu_items = {}

        for cmd in self.interface.commands:
            try:
                submenu = self._submenu(cmd.group, group_cache)
            except ValueError as exc:
                raise ValueError(
                    f"Command {cmd.text!r} does not belong to a current status "
                    "icon group."
                ) from exc
            else:
                if isinstance(cmd, Separator):
                    submenu.addSeparator()
                else:
                    submenu.addAction(cmd._impl.create_menu_item())
