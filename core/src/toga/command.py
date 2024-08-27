from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, MutableMapping, MutableSet, Protocol

from toga.handlers import simple_handler, wrapped_handler
from toga.icons import Icon
from toga.keys import Key
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.app import App
    from toga.icons import IconContentT

_py_id = id


class Group:
    def __init__(
        self,
        text: str,
        *,
        parent: Group | None = None,
        section: int = 0,
        order: int = 0,
        id: str | None = None,
    ):
        """
        A collection of commands to display together.

        :param text: A label for the group.
        :param parent: The parent of this group; use ``None`` to make a root group.
        :param section: The section where the group should appear within its parent. A
            section cannot be specified unless a parent is also specified.
        :param order: The position where the group should appear within its section.
            If multiple items have the same group, section and order, they will be
            sorted alphabetically by their text.
        :param id: A unique identifier for the group.
        """
        self._id = f"group-{_py_id(self)}" if id is None else id
        self._text = text
        self.order = order
        if parent is None and section != 0:
            raise ValueError("Section cannot be set without parent group")
        self.section = section

        # Prime the underlying value of _parent so that the setter has a current value
        # to work with
        self._parent: Group | None = None
        self.parent = parent

    @property
    def id(self) -> str:
        """A unique identifier for the group."""
        return self._id

    @property
    def text(self) -> str:
        """A text label for the group."""
        return self._text

    @property
    def parent(self) -> Group | None:
        """The parent of this group; returns ``None`` if the group is a root group."""
        return self._parent

    @parent.setter
    def parent(self, parent: Group | None) -> None:
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

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, (Group, Command)):
            return False
        return self.key < other.key

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, (Group, Command)):
            return False
        return other < self

    def __eq__(self, other: object) -> bool:
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
    def key(self) -> tuple[tuple[int, int, str], ...]:
        """A unique tuple describing the path to this group."""
        self_tuple = (self.section, self.order, self.text)
        if self.parent is None:
            return tuple([self_tuple])
        return tuple([*self.parent.key, self_tuple])

    # Standard groups - docstrings can only be provided within the `class` statement,
    # but the objects can't be instantiated here.
    APP: Group  #: Application-level commands
    FILE: Group  #: File commands
    EDIT: Group  #: Editing commands
    VIEW: Group  #: Content appearance commands
    COMMANDS: Group  #: Default group for user-provided commands
    WINDOW: Group  #: Window management commands
    HELP: Group  #: Help commands


Group.APP = Group("*", order=-100)
Group.FILE = Group("File", order=-30)
Group.EDIT = Group("Edit", order=-20)
Group.VIEW = Group("View", order=-10)
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


class Command:
    #: An identifier for the standard "About" menu item. This command is always
    #: installed by default. Uses :meth:`toga.App.about` as the default action.
    ABOUT: str = "about"
    #: An identifier for the standard "Exit" menu item. This command may be installed by
    #: default, depending on platform requirements. Uses :meth:`toga.App.request_exit`
    #: as the default action.
    EXIT: str = "request_exit"
    #: An identifier for the standard "New" menu item. This constant will be used for
    #: the default document type for your app; if you specify more than one document
    #: type, the command for the subsequent commands will have a colon and the first
    #: extension for that data type appended to the ID. Uses
    #: :meth:`toga.documents.DocumentSet.new` as the default action.
    NEW: str = "documents.new"
    #: An identifier for the standard "Open" menu item. This command will be
    #: automatically installed if your app declares any document types. Uses
    #: :meth:`toga.documents.DocumentSet.request_open` as the default action.
    OPEN: str = "documents.request_open"
    #: An identifier for the standard "Preferences" menu item. The Preferences item is
    #: not installed by default. If you install it manually, it will attempt to use
    #: ``toga.App.preferences()`` as the default action; your app will need to define
    #: this method, or provide an explicit value for the action.
    PREFERENCES: str = "preferences"
    #: An identifier for the standard "Save" menu item. This command will be
    #: automatically installed if your app declares any document types. Uses
    #: :meth:`toga.documents.DocumentSet.save` as the default action.
    SAVE: str = "documents.save"
    #: An identifier for the standard "Save As..." menu item. This command will be
    #: automatically installed if your app declares any document types. Uses
    #: :meth:`toga.documents.DocumentSet.save_as` as the default action.
    SAVE_AS: str = "documents.save_as"
    #: An identifier for the standard "Save All" menu item. This command will be
    #: automatically installed if your app declares any document types. Uses
    #: :meth:`toga.documents.DocumentSet.save_all` as the default action.
    SAVE_ALL: str = "documents.save_all"
    #: An identifier for the standard "Visit Homepage" menu item. This command may be
    #: installed by default, depending on platform requirements. Uses
    #: :meth:`toga.App.visit_homepage` as the default action.
    VISIT_HOMEPAGE: str = "visit_homepage"

    def __init__(
        self,
        action: ActionHandler | None,
        text: str,
        *,
        shortcut: str | Key | None = None,
        tooltip: str | None = None,
        icon: IconContentT | None = None,
        group: Group = Group.COMMANDS,
        section: int = 0,
        order: int = 0,
        enabled: bool = True,
        id: str = None,
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
        :param icon: The :any:`icon content <IconContentT>` that can be used to decorate
            the command if the platform requires.
        :param group: The group to which this command belongs.
        :param section: The section where the command should appear within its group.
        :param order: The position where the command should appear within its section.
            If multiple items have the same group, section and order, they will be
            sorted alphabetically by their text.
        :param enabled: Is the Command currently enabled?
        :param id: A unique identifier for the command.
        """
        self._id = f"cmd-{_py_id(self)}" if id is None else id
        self.text = text

        self.shortcut = shortcut
        self.tooltip = tooltip
        self.icon = icon

        self.group = group
        self.section = section
        self.order = order

        self.action = action

        self.factory = get_platform_factory()
        self._impl = self.factory.Command(interface=self)

        self._enabled = True
        self.enabled = enabled

    @classmethod
    def standard(cls, app: App, id, **kwargs):
        """Create an instance of a standard command for the provided app.

        The default action for the command will be constructed using the value of the
        command's ID as an attribute of the app object. If a method or co-routine
        matching that name doesn't exist, a value of ``None`` will be used as the
        default action.

        :param app: The app for which the standard command will be created.
        :param id: The ID of the standard command to create.
        :param kwargs: Overrides for any default properties of the standard command.
            Accepts the same arguments as the :class:`~toga.Command` constructor.
        """
        # The value of the ID constant is the method on the app instance
        cmd_kwargs = {"id": id}
        try:
            attrs = id.split(".")
            action = getattr(app, attrs[0])
            for attr in attrs[1:]:
                action = getattr(action, attr)
            cmd_kwargs["action"] = simple_handler(action)
        except AttributeError:
            cmd_kwargs["action"] = None

        # Get the platform-specific keyword arguments for the command
        factory = get_platform_factory()
        platform_kwargs = factory.Command.standard(app, id)

        if platform_kwargs:
            cmd_kwargs.update(platform_kwargs)
            cmd_kwargs.update(kwargs)

            # Return the command instance
            return Command(**cmd_kwargs)
        else:
            # Standard command doesn't exist on the platform.
            return None

    @property
    def id(self) -> str:
        """A unique identifier for the command."""
        return self._id

    @property
    def key(self) -> tuple[tuple[int, int, str], ...]:
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
    def enabled(self, value: bool) -> None:
        self._enabled = value and getattr(self.action, "_raw", True) is not None
        self._impl.set_enabled(value)

    @property
    def icon(self) -> Icon | None:
        """The Icon for the command.

        Can be specified as any valid :any:`icon content <IconContentT>`.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_or_name: IconContentT | None) -> None:
        if isinstance(icon_or_name, Icon) or icon_or_name is None:
            self._icon = icon_or_name
        else:
            self._icon = Icon(icon_or_name)

    @property
    def action(self) -> ActionHandler | None:
        """The Action attached to the command."""
        return self._action

    @action.setter
    def action(self, action: ActionHandler | None) -> None:
        """Set the action attached to the command

        Needs to be a valid ActionHandler or ``None``
        """
        self._action = wrapped_handler(self, action)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, (Group, Command)):
            return False
        return self.key < other.key

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, (Group, Command)):
            return False
        return other < self

    def __repr__(self) -> str:
        return (
            f"<Command text={self.text!r} "
            f"group={self.group} "
            f"section={self.section} "
            f"order={self.order}>"
        )


class Separator:
    def __init__(self, group: Group | None = None):
        """A representation of a separator between sections in a Group.

        :param group: The group that contains the separator.
        """
        self.group = group

    def __repr__(self) -> str:
        return f"<Separator group={None if self.group is None else self.group.text}>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Separator):
            return self.group == other.group
        return False


class CommandSetChangeHandler(Protocol):
    def __call__(self, **kwargs) -> object:
        """A handler that will be invoked when a Command or Group is added to the
        CommandSet.

        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class CommandSet(MutableSet[Command], MutableMapping[str, Command]):
    def __init__(
        self,
        on_change: CommandSetChangeHandler | None = None,
        app: App | None = None,
    ):
        """
        A collection of commands.

        This is used as an internal representation of Menus, Toolbars, and any other
        graphical manifestations of commands. You generally don't need to construct a
        CommandSet of your own; you should use existing app or window level CommandSet
        instances.

        The ``in`` operator can be used to evaluate whether a :class:`~toga.Command` is
        a member of the CommandSet, using either an instance of a Command, or the ID of
        a command.

        Commands can be retrieved from the CommandSet using ``[]`` notation with the
        requested command's ID.

        When iterated over, a CommandSet returns :class:`~toga.Command` instances in
        their sort order, with :class:`~toga.command.Separator` instances inserted
        between groups.

        :param on_change: A method that should be invoked when this CommandSet changes.
        :param app: The app this CommandSet is associated with, if it is not the app's
            own CommandSet.
        """
        self._app = app
        self._commands: dict[str:Command] = {}
        self.on_change = on_change

    def add(self, *commands: Command | None):
        """Add a collection of commands to the command set.

        A command value of ``None`` will be ignored. This allows you to add standard
        commands to a command set without first validating that the platform provides an
        implementation of that command.

        :param commands: The commands to add to the command set.
        """
        if self.app:
            self.app.commands.add(*commands)
        self._commands.update({cmd.id: cmd for cmd in commands if cmd is not None})
        if self.on_change:
            self.on_change()

    def clear(self) -> None:
        """Remove all commands from the command set."""
        self._commands = {}
        if self.on_change:
            self.on_change()

    @property
    def app(self) -> App | None:
        """The app this CommandSet is associated with.

        Returns None if this is the app's CommandSet.
        """
        return self._app

    def __contains__(self, obj: str | Command) -> Command:
        if isinstance(obj, Command):
            return obj in self._commands.values()
        else:
            return obj in self._commands

    def __getitem__(self, id: str) -> Command:
        return self._commands[id]

    def __setitem__(self, id: str, command: Command) -> Command:
        if id != command.id:
            raise ValueError(f"Command has id {command.id!r}; can't add as {id!r}")

        self.add(command)

    def __delitem__(self, id: str) -> Command:
        del self._commands[id]
        if self.on_change:
            self.on_change()

    def discard(self, command: Command):
        try:
            self._commands.pop(command.id)
            if self.on_change:
                self.on_change()
        except KeyError:
            pass

    def __len__(self) -> int:
        return len(self._commands)

    def __iter__(self) -> Iterator[Command | Separator]:
        cmd_iter = iter(sorted(self._commands.values()))

        def descendant(group: Group, ancestor: Group) -> Group | None:
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
