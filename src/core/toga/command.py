from toga.handlers import wrapped_handler
from toga.icons import Icon


class Group:
    """

    Args:
        label:
        order:
        parent:
    """
    def __init__(self, label, order=None, section=None, parent=None):
        self.label = label
        self.order = order if order else 0
        if parent is None and section is not None:
            raise ValueError("Section cannot be set without parent group")
        self.section = section if section else 0

        # First initialization needed for later
        self._parent = None
        self.parent = parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if parent is None:
            self._parent = None
            self._root = self
            return
        if parent == self or self.is_parent_of(parent):
            error_message = (
                'Cannot set {} to be a parent of {} '
                'because it causes a cyclic parenting.').format(
                parent.label, self.label
            )
            raise ValueError(error_message)
        self._parent = parent
        self._root = parent.root

    @property
    def root(self):
        return self._root

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

    def __hash__(self):
        return hash(self.to_tuple())

    def __lt__(self, other):
        return self.to_tuple() < other.to_tuple()

    def __gt__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        if other is None:
            return False
        return self.to_tuple() == other.to_tuple()

    def __repr__(self):
        parent_string = "None" if self.parent is None else self.parent.label
        return "<Group label={} parent={}>".format(
            self.label, parent_string
        )

    def to_tuple(self):
        self_tuple = (self.section, self.order, self.label)
        if self.parent is None:
            return tuple([self_tuple])
        return tuple([*self.parent.to_tuple(), self_tuple])


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
        self.sub_group = None
        self.section = section if section else 0
        self.order = order if order else 0

        self._impl = None
        self._build_impl()

        self.enabled = enabled and self.action is not None

    def bind(self, factory):
        self.factory = factory

        self._build_impl()

        if self._icon:
            self._icon.bind(self.factory)

        return self._impl

    def _build_impl(self):
        if self._impl is None and self.factory is not None:
            self._impl = self.factory.Command(interface=self)

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
        return self.to_tuple() < other.to_tuple()

    def __gt__(self, other):
        return not self.__lt__(other)

    def __repr__(self):
        return "<Command label={}>".format(self.label)

    def to_tuple(self):
        return tuple([*self.group.to_tuple(), (self.section, self.order, self.label)])


class DataSourceCommandSet(Command):

    def __init__(
            self,
            label,
            data,
            item_to_label,
            group=None,
            section=None,
            order=None,
            item_action=None,
            app=None,
            factory=None,
    ):
        super(DataSourceCommandSet, self).__init__(
            action=None,
            label=label,
            group=group,
            section=section,
            order=order,
            factory=factory
        )
        self.data = data
        self.item_action = item_action
        self.item_to_label = item_to_label
        self.app = app

        self.sub_group = Group(
            label=self.label, order=self.order, section=self.section, parent=self.group
        )

        self.data.add_listener(self)

    def __iter__(self):
        for index, item in enumerate(self.data):
            yield self.__build_command(index, item)

    def __repr__(self):
        return "<DataSourceCommandSet label={}>".format(self.label)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def item_action(self):
        return self._item_action

    @item_action.setter
    def item_action(self, item_action):
        self._item_action = item_action

    @property
    def item_to_label(self):
        return self._item_to_label

    @item_to_label.setter
    def item_to_label(self, item_to_label):
        self._item_to_label = item_to_label

    def insert(self, index, item):
        if self.app is not None:
            self.app._impl._update_data_menu_items(self)

    def remove(self, index, item):
        if self.app is not None:
            self.app._impl._update_data_menu_items(self)

    def __build_command(self, index, item):
        return Command(
            self.__get_action(item),
            self.item_to_label(item),
            group=self.sub_group,
            order=index,
            factory=self.factory
        )

    def __get_action(self, item):
        if self.item_action is None:
            return None
        return lambda widget: self.item_action(widget, item)


class Break:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<{self.name} break>".format(self=self)


GROUP_BREAK = Break('Group')
SECTION_BREAK = Break('Section')


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
