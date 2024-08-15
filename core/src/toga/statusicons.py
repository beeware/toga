from __future__ import annotations

import sys
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


class BaseStatusIcon:
    def __init__(self, icon: IconContentT | None = None, **kwargs):
        super().__init__(**kwargs)
        self.factory = get_platform_factory()
        self._impl = getattr(self.factory, self.__class__.__name__)(interface=self)

        self.icon = icon

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

    def _create(self):
        pass


class StatusIcon(BaseStatusIcon):
    def __init__(
        self,
        id: str | None = None,
        icon: IconContentT | None = None,
        on_press: toga.widgets.button.OnPressHandler | None = None,
    ):
        """
        An button in a status bar or system tray.

        When pressed, the ``on_press`` handler will be activated.

        :param id: An identifier for the status icon.
        :param icon: The icon, or icon resource, that will be displayed in the status
            bar or system tray.
        :param on_press: The handler to invoke when the status icon is pressed.
        """
        super().__init__(icon=icon)
        self.on_press = on_press
        self._id = f"status_icon-{_py_id(self)}" if id is None else id

    @property
    def id(self) -> str:
        """A unique identifier for the group."""
        return self._id

    @property
    def on_press(self) -> toga.widgets.button.OnPressHandler:
        """The handler to invoke when the status icon is pressed."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler: toga.widgets.button.OnPressHandler) -> None:
        self._on_press = wrapped_handler(self, handler)


class MenuStatusIcon(BaseStatusIcon, Group):
    def __init__(
        self,
        id: str | None = None,
        icon: IconContentT | None = None,
        standard_commands=True,
    ):
        """
        An item in a status bar or system tray that displays a menu when pressed.

        A ``MenuStatusIcon`` can be used as a :class:`~toga.Group` when defining
        :class:`toga.Command` instances. It will have ordering priority equivalent to
        :attr:`~toga.Group.COMMANDS`.

        :param id: An identifier for the status icon.
        :param icon: The icon, or icon resource, that will be displayed in the status
            bar or system tray.
        :param standard_commands: Should the standard menu commands be installed into
            the menu?
        """
        super().__init__(
            id=id,
            icon=icon,
            order=Group.COMMANDS.order,
            text=f"Menu Status Icon {id if id else _py_id(self)}",
        )
        self.commands = CommandSet()

        if standard_commands:
            # Create the standard commands for the menu status icon.
            # Use the default standard constructor, but force the commands
            # into the last section of *this* group for ordering purposes.
            for cmd_id in [
                Command.ABOUT,
                Command.EXIT,
            ]:
                self.commands.add(
                    Command.standard(
                        toga.App.app,
                        cmd_id,
                        section=sys.maxsize,
                        group=self,
                    )
                )

    def __repr__(self):
        return f"<{self.text}>"

    def _create(self):
        super()._create()

        # Create the menus for the status icon, and install a handler to respond to
        # command changes.
        self._impl.create_menus()
        self.commands.on_change = self._impl.create_menus


class StatusIconSet(Sequence[StatusIcon], Mapping[str, StatusIcon]):
    def __init__(self):
        """A collection of status icons."""
        self.elements: dict[str, StatusIcon] = {}

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
        for status_icon in status_icons:
            if status_icon.id not in self.elements:
                self.elements[status_icon.id] = status_icon
                status_icon._impl.create()

    def remove(self, status_icon: StatusIcon):
        try:
            self.elements.pop(status_icon.id)
            status_icon._impl.remove()
        except KeyError:
            raise ValueError("Not a known status icon.")
