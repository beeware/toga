from __future__ import annotations

from typing import TYPE_CHECKING

from toga.handlers import wrapped_handler
from toga.icons import Icon
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.window import Window


class Group:
    def __init__(
        self,
        text,
        order=None,
        section=None,
        parent=None,
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
        :param section: An integer describing the section within the group where the
            command should appear. If no section is specified, the command will be
            allocated to section 0 within the group.
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
            self._root = self
            return
        if parent == self or self.is_parent_of(parent):
            error_message = (
                f"Cannot set {parent.text} to be a parent of {self.text} "
                "because it causes a cyclic parenting."
            )
            raise ValueError(error_message)
        self._parent = parent
        self._root = parent.root

    @property
    def root(self) -> Group:
        """The root group for this group.

        This will be ``self`` if the group *is* a root group."""
        return self._root

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

    def is_child_of(self, parent):
        """Is this group a child of the provided group?

        :param parent: The potential parent to check
        :returns: True if this group is a child of the provided parent.
        """
        return parent.is_parent_of(self)

    def __hash__(self):
        return hash(self.key)

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return other < self

    def __eq__(self, other):
        if other is None:
            return False
        return self.key == other.key

    def __repr__(self):
        parent_string = "None" if self.parent is None else self.parent.text
        return "<Group text={} order={} parent={}>".format(
            self.text, self.order, parent_string
        )

    @property
    def key(self) -> tuple[(int, int, str)]:
        """A unique tuple describing the path to this group."""
        self_tuple = (self.section, self.order, self.text)
        if self.parent is None:
            return tuple([self_tuple])
        return tuple([*self.parent.key, self_tuple])

    @property
    def path(self) -> list[Group]:
        """A list containing the chain of groups that contain this group."""
        if self.parent is None:
            return [self]
        return [*self.parent.path, self]


Group.APP = Group("*", order=0)
Group.FILE = Group("File", order=1)
Group.EDIT = Group("Edit", order=10)
Group.VIEW = Group("View", order=20)
Group.COMMANDS = Group("Commands", order=30)
Group.WINDOW = Group("Window", order=90)
Group.HELP = Group("Help", order=100)


class Command:
    def __init__(
        self,
        action,
        text,
        shortcut=None,
        tooltip=None,
        icon=None,
        group=None,
        section=None,
        order=None,
        enabled=True,
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
    def enabled(self, value):
        self._enabled = value
        if self._impl is not None:
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

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return other < self

    def __repr__(self):
        return "<Command text={} group={} section={} order={}>".format(
            self.text,
            self.group,
            self.section,
            self.order,
        )


class Break:
    def __init__(self, name):
        """A representation of a separator between Command Groups, or between sections
        in a Group.
        """
        self.name = name

    def __repr__(self):
        return f"<{self.name} break>"


GROUP_BREAK = Break("Group")
SECTION_BREAK = Break("Section")


class CommandSet:
    def __init__(self, window: Window = None, on_change=None):
        """
        A collection of commands.

        This is used as an internal representation of Menus, Toolbars, and any other
        graphical manifestations of commands.

        The collection can be iterated over to provide the display order of the commands
        managed by the group.

        :param window: The window with which this CommandSet is associated.
        :param on_change: A method that should be invoked when this command set changes.
        """
        self.window = window
        self._commands = set()
        self.on_change = on_change

    def add(self, *commands):
        if self.window and self.window.app is not None:
            self.window.app.commands.add(*commands)
        self._commands.update(commands)
        if self.on_change:
            self.on_change()

    def __len__(self):
        return len(self._commands)

    def __iter__(self):
        prev_cmd = None
        for cmd in sorted(self._commands):
            if prev_cmd:
                if cmd.group != prev_cmd.group:
                    yield GROUP_BREAK
                elif cmd.section != prev_cmd.section:
                    yield SECTION_BREAK

            yield cmd
            prev_cmd = cmd
