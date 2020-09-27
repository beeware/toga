from toga.handlers import wrapped_handler
from toga.icons import Icon


class Group:
    """

    Args:
        label:
        order:
        parent:
    """
    def __init__(self, label, order=None, section=None, parent=None, children=None):
        self.label = label
        self.order = order if order else 0
        if parent is None and section is not None:
            raise ValueError("Section cannot be set without parent group")
        self.section = section if section else 0

        # First initialization needed for later
        self._parent = None
        self._children = []

        try:
            self.parent = parent
            self.children = children
        except ValueError as error:
            self.parent = None
            self.children = None
            raise error

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if parent == self or self.is_parent_of(parent):
            self.__raise_parent_error(parent, self)
        old_parent = self.parent
        self._parent = parent
        if old_parent is not None:
            old_parent.remove_child(self)
        if parent is not None:
            parent.add_child(self)

    @property
    def children(self):
        # Returning copy in order to keep internal data safe
        return list(self._children)

    @children.setter
    def children(self, children):
        if children is None:
            children = []
        invalid_children = [
            child for child in children
            if child == self or child.is_parent_of(self)
        ]
        if len(invalid_children) != 0:
            self.__raise_parent_error(self, invalid_children[0])
        for child in self.children:
            child.parent = None
        self._children = []
        for child in children:
            self.add_child(child)

    def add_child(self, child):
        if child == self or child.is_parent_of(self):
            self.__raise_parent_error(self, child)
        if child.parent != self:
            child.parent = self
        if child not in self._children:
            self._children.append(child)

    def remove_child(self, child):
        if child.parent == self:
            child.parent = None
        if child in self._children:
            self._children.remove(child)

    def is_parent_of(self, child):
        if child is None:
            return False
        if child.parent is None:
            return False
        if child.parent == self:
            return True
        return self.is_parent_of(child.parent)

    def is_child_of(self, parent):
        return parent.is_parent_of(self)

    def __lt__(self, other):
        if self.parent == other.parent:
            return [self.section, self.order, self.label] < [
                other.section, other.order, other.label
            ]
        if self.is_parent_of(other):
            return True
        if other.is_parent_of(self):
            return False
        if self.parent is None:
            return self < other.parent
        if other.parent is None:
            return self.parent < other
        return self.parent < other.parent

    def __gt__(self, other):
        return other < self

    def __eq__(self, other):
        if other is None:
            return False
        return self.order == other.order and self.label == other.label

    def __repr__(self):
        parent_string = self.__to_string(self.parent)
        children_strings = "[" + ", ".join(
            [self.__to_string(child) for child in self.children]
        ) + "]"
        return "Group[label={}, order={}, parent={}, children={}]".format(
            self.label, self.order, parent_string, children_strings
        )

    @classmethod
    def __to_string(cls, group):
        if group is None:
            return "None"
        return group.label

    @classmethod
    def __raise_parent_error(cls, parent, child):
        error_message = 'Cannot set {} to be a parent of {} because it causes a cyclic parenting.'.format(
            parent.label, child.label
        )
        raise ValueError(error_message)


Group.APP = Group('*', order=0)
Group.FILE = Group('File', order=1)
Group.EDIT = Group('Edit', order=10)
Group.VIEW = Group('View', order=20)
Group.COMMANDS = Group('Commands', order=30)
Group.WINDOW = Group('Window', order=90)
Group.HELP = Group('Help', order=100)


class Command:
    """
    Args:
        action: a function to invoke when the command is activated.
        label: a name for the command.
        shortcut: (optional) a key combination that can be used to invoke the
            command.
        tooltip: (optional) a short description for what the command will do.
        icon: (optional) a path to an icon resource to decorate the command.
        group: (optional) a Group object describing a collection of similar
            commands. If no group is specified, a default "Command" group will
            be used.
        section: (optional) an integer providing a sub-grouping. If no section
            is specified, the command will be allocated to section 0 within the
            group.
        order: (optional) an integer indicating where a command falls within a
            section. If a Command doesn't have an order, it will be sorted
            alphabetically by label within its section.
        enabled: whether to enable the command or not.
    """
    def __init__(self, action, label,
                 shortcut=None, tooltip=None, icon=None,
                 group=None, section=None, order=None, enabled=True, factory=None):
        self.factory = factory

        self.action = wrapped_handler(self, action)
        self.label = label

        self.shortcut = shortcut
        self.tooltip = tooltip
        self.icon = icon

        self.group = group if group else Group.COMMANDS
        self.section = section if section else 0
        self.order = order if order else 0

        self._impl = None

        self.enabled = enabled and self.action is not None

    def bind(self, factory):
        self.factory = factory

        if self._impl is None:
            self._impl = self.factory.Command(interface=self)

        if self._icon:
            self._icon.bind(self.factory)

        return self._impl

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        if self._impl is not None:
            self._impl.set_enabled(value)

    @property
    def icon(self):
        """
        The Icon for the app.

        :returns: A ``toga.Icon`` instance for the app's icon.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_or_name):
        if isinstance(icon_or_name, Icon) or icon_or_name is None:
            self._icon = icon_or_name
        else:
            self._icon = Icon(icon_or_name)

        if self._icon and self.factory:
            self._icon.bind(self.factory)

    def __lt__(self, other):
        if self.group == other.group:
            return [self.section, self.order, self.label] < [
                other.section, other.order, other.label
            ]
        if self.group == other.group.parent:
            return [self.section, self.order, self.label] < [
                other.group.section,
                other.group.order,
                other.group.label,
            ]
        if self.group.parent == other.group:
            return [self.group.section, self.group.order, self.group.label] < [
                other.section, other.order, other.label
            ]
        return self.group < other.group

    def __gt__(self, other):
        return other < self

    def __repr__(self):
        return "Command[label={}, group={}, section={}, order={}]".format(
            self.label,
            self.group.parent,
            self.section,
            self.order,
        )


GROUP_BREAK = object()
SECTION_BREAK = object()


class CommandSet:
    """

    Args:
        factory:
        widget:
        on_change:

    Todo:
        * Add missing Docstrings.
    """
    def __init__(self, factory, widget=None, on_change=None):
        self.factory = factory
        self.widget = widget
        self._commands = set()
        self.on_change = on_change

    def add(self, *commands):
        for cmd in commands:
            cmd.bind(self.factory)
        if self.widget and self.widget.app is not None:
            self.widget.app.commands.add(*commands)
        self._commands.update(commands)
        if self.on_change:
            self.on_change()

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
