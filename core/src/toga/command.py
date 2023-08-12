from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

from toga.handlers import wrapped_handler
from toga.icons import Icon
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.app import App


class Group:
    def __init__(
        self,
        text: str,
        order: int | None = None,
        section: int | None = None,
        parent: Group | None = None,
    ):
        """
        An collection of similar commands.

        Commands and sub-groups are sorted within sections inside a group.

        Groups can also be hierarchical; a group with no parent is a root group.

        :param text: The name of the group
        :param order: An integer that can be used to provide sorting order for commands.
            Commands will be sorted according to order inside their section; if a
            Command doesn't have an order, it will be sorted alphabetically by text
            within its section.
        :param section: An integer describing the section within the parent group where
            the command should appear. If no section is specified, the command will be
            allocated to section 0 within the group. A section cannot be specified
            unless a parent is also specified.
        :param parent: The parent of this group; use ``None`` to describe a root group.
        """
        self.text = text
        self.order = order if order else 0
        if parent is None and section is not None:
            raise ValueError("Section cannot be set without parent group")
        self.section = section if section else 0

        # Prime the underlying value of _parent so that the setter has a current value
        # to work with
        self._parent = None
        self.parent = parent

    @property
    def parent(self) -> Group | None:
        """The parent of this group; returns ``None`` if the group is a root group"""
        return self._parent

    @parent.setter
    def parent(self, parent: Group | None):
        if parent is None:
            self._parent = None
        elif parent == self:
            raise ValueError("A group cannot be it's own parent")
        elif self.is_parent_of(parent):
            raise ValueError(
                f"Cannot set parent; {self.text!r} is an ancestor of {parent.text!r}."
            )
        else:
            self._parent = parent

    @property
    def root(self) -> Group:
        """The root group for this group.

        This will be ``self`` if the group *is* a root group."""
        if self.parent is None:
            return self
        return self.parent.root

    def is_parent_of(self, child: Group | None) -> bool:
        """Is this group a parent of the provided group?

        :param child: The potential child to check
        :returns: True if this group is a parent of the provided child.
        """
        if child is None:
            return False
        if child.parent is None:
            return False
        if child.parent == self:
            return True
        return self.is_parent_of(child.parent)

    def is_child_of(self, parent: Group | None) -> bool:
        """Is this group a child of the provided group?

        :param parent: The potential parent to check
        :returns: True if this group is a child of the provided parent.
        """
        if parent is None:
            return False
        return parent.is_parent_of(self)

    def __hash__(self) -> int:
        return hash(self.key)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, (Group, Command)):
            return False
        return self.key < other.key

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, (Group, Command)):
            return False
        return other < self

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, (Group, Command)):
            return False
        return self.key == other.key

    def __repr__(self) -> str:
        parent_string = (
            f" parent={self.parent} section={self.section}"
            if self.parent is not None
            else ""
        )
        return f"<Group text={self.text!r} order={self.order}{parent_string}>"

    @property
    def key(self) -> tuple[(int, int, str)]:
        """A unique tuple describing the path to this group."""
        self_tuple = (self.section, self.order, self.text)
        if self.parent is None:
            return tuple([self_tuple])
        return tuple([*self.parent.key, self_tuple])


Group.APP = Group("*", order=0)
Group.FILE = Group("File", order=1)
Group.EDIT = Group("Edit", order=10)
Group.VIEW = Group("View", order=20)
Group.COMMANDS = Group("Commands", order=30)
Group.WINDOW = Group("Window", order=90)
Group.HELP = Group("Help", order=100)


class ActionHandler(Protocol):
    def __call__(self, command: Command, **kwargs) -> bool:
        """A handler that will be invoked when a Command is invoked.

        .. note::
            ``**kwargs`` ensures compatibility with additional arguments
            introduced in future versions.

        :param command: The command that triggered the action.
        """
        ...


class Command:
    def __init__(
        self,
        action: ActionHandler | None,
        text: str,
        shortcut: str | None = None,
        tooltip: str | None = None,
        icon: str | Icon | None = None,
        group: Group | None = None,
        section: int | None = None,
        order: int | None = None,
        enabled: bool = True,
    ):
        """
        Create a new Command.

        :param action: A handler that will be invoked when the command is activated.
        :param text: A text label for the command.
        :param shortcut: A key combination that can be used to invoke the command.
        :param tooltip: A short description for what the command will do.
        :param icon: The icon, or icon resource, that can be used to decorate the
            command if the platform requires.
        :param group: The group of commands to which this command belongs. If no group
            is specified, a default "Command" group will be used.
        :param section: An integer describing the section within the group where the
            command should appear. If no section is specified, the command will be
            allocated to section 0 within the group.
        :param order: An integer that can be used to provide sorting order for commands.
            Commands will be sorted according to order inside their section; if a
            Command doesn't have an order, it will be sorted alphabetically by text within its section.
        :param enabled: Is the Command currently enabled?
        """
        self.text = text

        self.shortcut = shortcut
        self.tooltip = tooltip
        self.icon = icon

        self.group = group if group else Group.COMMANDS
        self.section = section if section else 0
        self.order = order if order else 0

        orig_action = action
        self.action = wrapped_handler(self, action)

        self.factory = get_platform_factory()
        self._impl = self.factory.Command(interface=self)

        self.enabled = enabled and orig_action is not None

    @property
    def key(self) -> tuple[(int, int, str)]:
        """A unique tuple describing the path to this command.

        Each element in the tuple describes the (section, order, text) for the
        groups that must be navigated to invoke this action.
        """
        return tuple([*self.group.key, (self.section, self.order, self.text)])

    @property
    def enabled(self) -> bool:
        """Is the command currently enabled?"""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        self._impl.set_enabled(value)

    @property
    def icon(self) -> Icon | None:
        """The Icon for the command.

        When specifying the icon, you can provide an icon instance, or a string resource
        that can be resolved to an icon.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_or_name: str | Icon):
        if isinstance(icon_or_name, Icon) or icon_or_name is None:
            self._icon = icon_or_name
        else:
            self._icon = Icon(icon_or_name)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, (Group, Command)):
            return False
        return self.key < other.key

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, (Group, Command)):
            return False
        return other < self

    def __repr__(self) -> bool:
        return (
            f"<Command text={self.text!r} "
            f"group={self.group} "
            f"section={self.section} "
            f"order={self.order}>"
        )


class Break:
    def __init__(self, name: str):
        """A representation of a separator between Command Groups, or between sections
        in a Group.

        :param name: A name of the break type.
        """
        self.name = name

    def __repr__(self) -> str:
        return f"<{self.name} break>"


GROUP_BREAK = Break("Group")
SECTION_BREAK = Break("Section")


class CommandSetChangeHandler(Protocol):
    def __call__(self) -> None:
        """A handler that will be invoked when a Command or Group is added to the CommandSet.

        .. note::
            ``**kwargs`` ensures compatibility with additional arguments
            introduced in future versions.

        :return: Nothing
        """
        ...


class CommandSet:
    def __init__(self, on_change: CommandSetChangeHandler = None):
        """
        A collection of commands.

        This is used as an internal representation of Menus, Toolbars, and any other
        graphical manifestations of commands. You generally don't need to construct a
        CommandSet of your own; you should use existing app or window level CommandSet
        instances.

        The collection can be iterated over to provide the display order of the commands
        managed by the group.

        :param on_change: A method that should be invoked when this command set changes.
        """
        self._app = None
        self._commands = set()
        self.on_change = on_change

    def add(self, *commands: Command | Group):
        if self.app and self.app is not None:
            self.app.commands.add(*commands)
        self._commands.update(commands)
        if self.on_change:
            self.on_change()

    @property
    def app(self) -> App:
        return self._app

    @app.setter
    def app(self, value: App):
        self._app = value
        self._app.commands.add(*self._commands)

    def __len__(self) -> int:
        return len(self._commands)

    def __iter__(self) -> Command | Group | Break:
        prev_cmd = None
        for cmd in sorted(self._commands):
            if prev_cmd:
                if cmd.group != prev_cmd.group:
                    yield GROUP_BREAK
                elif cmd.section != prev_cmd.section:
                    yield SECTION_BREAK

            yield cmd
            prev_cmd = cmd
