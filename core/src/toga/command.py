from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

from toga.handlers import wrapped_handler
from toga.icons import Icon
from toga.keys import Key
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.app import App
    from toga.icons import IconContent


class Group:
    def __init__(
        self,
        text: str,
        *,
        parent: Group | None = None,
        section: int = 0,
        order: int = 0,
    ):
        """
        An collection of commands to display together.

        :param text: A label for the group.
        :param parent: The parent of this group; use ``None`` to make a root group.
        :param section: The section where the group should appear within its parent. A
            section cannot be specified unless a parent is also specified.
        :param order: The position where the group should appear within its section.
            If multiple items have the same group, section and order, they will be
            sorted alphabetically by their text.
        """
        self.text = text
        self.order = order
        if parent is None and section != 0:
            raise ValueError("Section cannot be set without parent group")
        self.section = section

        # Prime the underlying value of _parent so that the setter has a current value
        # to work with
        self._parent = None
        self.parent = parent

    @property
    def parent(self) -> Group | None:
        """The parent of this group; returns ``None`` if the group is a root group."""
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
        """Is this group a parent of the provided group, directly or indirectly?

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
        """Is this group a child of the provided group, directly or indirectly?

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

    # Standard groups - docstrings can only be provided within the `class` statement,
    # but the objects can't be instantiated here.
    APP = None  #: Application-level commands
    FILE = None  #: File commands
    EDIT = None  #: Editing commands
    VIEW = None  #: Content appearance commands
    COMMANDS = None  #: Default group for user-provided commands
    WINDOW = None  #: Window management commands
    HELP = None  #: Help commands


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

        :param command: The command that triggered the action.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        """
        ...


class Command:
    def __init__(
        self,
        action: ActionHandler | None,
        text: str,
        *,
        shortcut: str | Key | None = None,
        tooltip: str | None = None,
        icon: IconContent | None = None,
        group: Group = Group.COMMANDS,
        section: int = 0,
        order: int = 0,
        enabled: bool = True,
    ):
        """
        Create a new Command.

        Commands may not use all the arguments - for example, on some platforms, menus
        will contain icons; on other platforms they won't.

        :param action: A handler to invoke when the command is activated. If this is
            ``None``, the command will be disabled.
        :param text: A label for the command.
        :param shortcut: A key combination that can be used to invoke the command.
        :param tooltip: A short description of what the command will do.
        :param icon: The :any:`icon content <IconContent>` that can be used to decorate
            the command if the platform requires.
        :param group: The group to which this command belongs.
        :param section: The section where the command should appear within its group.
        :param order: The position where the command should appear within its section.
            If multiple items have the same group, section and order, they will be
            sorted alphabetically by their text.
        :param enabled: Is the Command currently enabled?
        """
        self.text = text

        self.shortcut = shortcut
        self.tooltip = tooltip
        self.icon = icon

        self.group = group
        self.section = section
        self.order = order

        self.action = wrapped_handler(self, action)

        self.factory = get_platform_factory()
        self._impl = self.factory.Command(interface=self)

        self.enabled = enabled

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
        self._enabled = value and getattr(self.action, "_raw", True) is not None
        self._impl.set_enabled(value)

    @property
    def icon(self) -> Icon | None:
        """The Icon for the command.

        Can be specified as any valid :any:`icon content <IconContent>`.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_or_name: IconContent | None):
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


class Separator:
    def __init__(self, group: Group = None):
        """A representation of a separator between sections in a Group.

        :param group: The group that contains the separator.
        """
        self.group = group

    def __repr__(self) -> str:
        return f"<Separator group={self.group.text}>"

    def __eq__(self, other) -> bool:
        if isinstance(other, Separator):
            return self.group == other.group
        return False


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
    def __init__(
        self,
        on_change: CommandSetChangeHandler = None,
        app: App | None = None,
    ):
        """
        A collection of commands.

        This is used as an internal representation of Menus, Toolbars, and any other
        graphical manifestations of commands. You generally don't need to construct a
        CommandSet of your own; you should use existing app or window level CommandSet
        instances.

        The collection can be iterated over to provide the display order of the commands
        managed by the group.

        :param on_change: A method that should be invoked when this command set changes.
        :param app: The app this command set is associated with, if it is not the app's
            own commandset.
        """
        self._app = app
        self._commands = set()
        self.on_change = on_change

    def add(self, *commands: Command | Group):
        if self.app and self.app is not None:
            self.app.commands.add(*commands)
        self._commands.update(commands)
        if self.on_change:
            self.on_change()

    def clear(self):
        self._commands = set()
        if self.on_change:
            self.on_change()

    @property
    def app(self) -> App:
        return self._app

    def __len__(self) -> int:
        return len(self._commands)

    def __iter__(self) -> Command | Separator:
        cmd_iter = iter(sorted(self._commands))

        def descendant(group, ancestor):
            # Return the immediate descendant of ancestor used by this group.
            if group.parent == ancestor:
                return group
            if group.parent:
                return descendant(group.parent, ancestor)
            return None

        # The iteration over commands tells us the exact order of commands, but doesn't
        # tell us anything about menu and submenu structure. In order to insert section
        # breaks in the right place (including before and after submenus), we need to
        # iterate over commands inside each group, dealing with each subgroup as an
        # independent iteration.
        #
        # The iterator over commands is maintained external to this recursive iteration,
        # because we may need to inspect the command at multiple group levels, but we
        # can't `peek` at the top element of an iterator, `push` an item back on after
        # it has been consumed, or pass the consumed item as a return value in addition
        # to the generator result.
        def _iter_group(parent):
            nonlocal command
            nonlocal finished
            section = None

            def _section_break(obj):
                # Utility method that will insert a section break, if required.
                # A section break is needed if the section for the object we're
                # processing (either a command, or a group acting as a submenu)
                # has a section ID different to the previous object processed at
                # this level, excluding the very first object (as there's no need
                # for a section break before the first command/submenu).
                nonlocal section
                if section is not None:
                    if section != obj.section:
                        yield Separator(parent)
                        section = obj.section
                else:
                    section = obj.section

            while not finished:
                if parent is None:
                    # Handle root-level menus
                    yield from _iter_group(command.group.root)
                elif command.group == parent:
                    # A normal command at this level of the group.
                    yield from _section_break(command)
                    yield command

                    # Consume the next item on the iterator; if we run out, mark the
                    # sentinel that says we've finished. We can't just raise
                    # StopIteration, because that stops the *generator* we're creating.
                    try:
                        command = next(cmd_iter)
                    except StopIteration:
                        finished = True
                else:
                    # The command isn't in this group. If the command is in descendant
                    # group, yield items from the group. If it's not a descendant, then
                    # there are no more commands in this group; we can return to the
                    # previous group for processing.
                    subgroup = descendant(command.group, parent)
                    if subgroup:
                        yield from _section_break(subgroup)
                        yield from _iter_group(subgroup)
                    else:
                        return

        # Prime the initial command into the command iterator
        try:
            command = next(cmd_iter)
        except StopIteration:
            pass
        else:
            finished = False
            yield from _iter_group(None)
