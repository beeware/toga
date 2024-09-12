from __future__ import annotations

import sys
from abc import abstractmethod
from collections.abc import Iterator
from typing import TYPE_CHECKING, Mapping, Sequence

import toga
from toga.command import Command, CommandSet, Group
from toga.handlers import wrapped_handler
from toga.icons import Icon
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.icons import IconContentT

_py_id = id


class StatusIcon:
    def __init__(self, icon: IconContentT | None = None):
        """An abstract base class for all status icons."""
        self.factory = get_platform_factory()
        self._impl = getattr(self.factory, self.__class__.__name__)(interface=self)

        self.icon = icon

    @property
    @abstractmethod
    def id(self) -> str:
        """A unique identifier for the status icon."""

    @property
    @abstractmethod
    def text(self) -> str:
        """A text label for the status icon."""

    @property
    def icon(self) -> Icon | None:
        """The Icon to display in the status bar.

        When setting the icon, you can provide either an :any:`Icon` instance, or a
        path that will be passed to the ``Icon`` constructor.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_or_name: IconContentT | None):
        if isinstance(icon_or_name, Icon) or icon_or_name is None:
            self._icon = icon_or_name
        else:
            self._icon = Icon(icon_or_name)

        self._impl.set_icon(self._icon)


class SimpleStatusIcon(StatusIcon):
    def __init__(
        self,
        id: str | None = None,
        icon: IconContentT | None = None,
        text: str | None = None,
        on_press: toga.widgets.button.OnPressHandler | None = None,
    ):
        """
        An button in a status bar or system tray.

        When pressed, the ``on_press`` handler will be activated.

        :param id: An identifier for the status icon.
        :param icon: The icon, or icon resource, that will be displayed in the status
            bar or system tray.
        :param text: A text label for the status icon. Defaults to the formal name of
            the app.
        :param on_press: The handler to invoke when the status icon is pressed.
        """
        super().__init__(icon=icon)
        self.on_press = on_press

        self._id = f"statusicon-{_py_id(self)}" if id is None else id
        self._text = text if text is not None else toga.App.app.formal_name

    def __repr__(self):
        return f"<SimpleStatusIcon {self.text!r}: {self.id}>"

    @property
    def id(self) -> str:
        return self._id

    @property
    def text(self) -> str:
        return self._text

    @property
    def on_press(self) -> toga.widgets.button.OnPressHandler:
        """The handler to invoke when the status icon is pressed."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler: toga.widgets.button.OnPressHandler) -> None:
        self._on_press = wrapped_handler(self, handler)


class MenuStatusIcon(Group, StatusIcon):
    def __init__(
        self,
        id: str | None = None,
        icon: IconContentT | None = None,
        text: str | None = None,
    ):
        """
        An item in a status bar or system tray that displays a menu when pressed.

        A ``MenuStatusIcon`` can be used as a :class:`~toga.Group` when defining
        :class:`toga.Command` instances.

        :param id: An identifier for the status icon.
        :param icon: The icon, or icon resource, that will be displayed in the status
            bar or system tray.
        :param text: A text label for the status icon. Defaults to the formal name of
            the app.
        """
        Group.__init__(
            self,
            id=f"menustatusitem-{_py_id(self)}" if id is None else id,
            text=(text if text is not None else toga.App.app.formal_name),
        )
        StatusIcon.__init__(self, icon=icon)

    def __repr__(self):
        return f"<MenuStatusIcon {self.text!r}: {self.id}>"


class StatusIconSet(Sequence[StatusIcon], Mapping[str, StatusIcon]):
    def __init__(self):
        """An ordered collection of status icons.

        The items in the set can be retrieved by instance, or by ID. When iterated, the
        items are returned in the order they were added.
        """
        self.factory = get_platform_factory()
        self._impl = self.factory.StatusIconSet(interface=self)

        self.elements: dict[str, StatusIcon] = {}
        self.commands = CommandSet()

    @property
    def _menu_status_icons(self):
        """An iterator over the menu status icons that have been registered."""
        return (icon for icon in self if isinstance(icon, MenuStatusIcon))

    @property
    def _primary_menu_status_icon(self):
        """The first menu status icon that has been registered.

        Returns ``None`` if no menu status icons have been registered.
        """
        try:
            return next(self._menu_status_icons)
        except StopIteration:
            # No menu status icons registered.
            return None

    def _create_standard_commands(self):
        # Create the standard commands for the menu status icon. Use the standard
        # constructor, but force the commands into *last* section of the COMMANDS group
        # so they'll appear on the first MenuStatusIcon.
        for cmd_id in [
            Command.ABOUT,
            Command.EXIT,
        ]:
            self.commands.add(
                Command.standard(
                    toga.App.app,
                    cmd_id,
                    section=sys.maxsize,
                    group=Group.COMMANDS,
                )
            )

    def __iter__(self) -> Iterator[StatusIcon]:
        return iter(self.elements.values())

    def __contains__(self, value: object) -> bool:
        if isinstance(value, str):
            return value in self.elements.keys()
        else:
            return value in self.elements.values()

    def __len__(self) -> int:
        return len(self.elements)

    def __getitem__(self, index_or_id):
        if isinstance(index_or_id, int):
            return list(self.elements.values())[index_or_id]
        else:
            return self.elements[index_or_id]

    def add(self, *status_icons: StatusIcon):
        """Add one or more icons to the set.

        :param status_icons: The icon (or icons) to add to the set.
        """
        added = False
        for status_icon in status_icons:
            if status_icon.id not in self.elements:
                self.elements[status_icon.id] = status_icon
                status_icon._impl.create()
                added = True

        if added and self.commands.on_change:
            self.commands.on_change()

    def remove(self, status_icon: StatusIcon):
        """Remove a single icon from the set.

        :param status_icon: The status icon instance to remove.
        :raises ValueError: If the status icon commands include any commands that
            reference the icon that has been removed.
        """
        try:
            self.elements.pop(status_icon.id)
            status_icon._impl.remove()

            if self.commands.on_change:
                self.commands.on_change()
        except KeyError:
            raise ValueError("Not a known status icon.")

    def clear(self):
        """Remove all the icons from the set.

        :raises ValueError: If the status icon commands include any commands that
            reference an icon that has been removed.
        """
        # Convert into a list so that we're not deleting from a list while iterating.
        for status_icon in list(self):
            self.elements.pop(status_icon.id)
            status_icon._impl.remove()

        if self.commands.on_change:
            self.commands.on_change()
