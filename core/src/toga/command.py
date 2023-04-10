import warnings

from toga.handlers import wrapped_handler
from toga.icons import Icon
from toga.platform import get_platform_factory

# BACKWARDS COMPATIBILITY: a token object that can be used to differentiate
# between an explicitly provided ``None``, and an unspecified value falling
# back to a default.
NOT_PROVIDED = object()


class Group:
    """

    Args:
        text:
        order:
        parent:
    """

    def __init__(
        self,
        text=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
        # can be removed when the handling for
        # `label` is removed
        order=None,
        section=None,
        parent=None,
        label=None,  # DEPRECATED!
    ):
        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################
        # When deleting this block, also delete the NOT_PROVIDED
        # placeholder, and replace its usage in default values.

        # label replaced with text
        if label is not None:
            if text is not NOT_PROVIDED:
                raise ValueError(
                    "Cannot specify both `label` and `text`; "
                    "`label` has been deprecated, use `text`"
                )
            else:
                warnings.warn(
                    "Group.label has been renamed Group.text", DeprecationWarning
                )
                text = label
        elif text is NOT_PROVIDED:
            # This would be raised by Python itself; however, we need to use a placeholder
            # value as part of the migration from text->value.
            raise TypeError(
                "Group.__init__ missing 1 required positional argument: 'text'"
            )

        ##################################################################
        # End backwards compatibility.
        ##################################################################

        self.text = text
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
                "Cannot set {} to be a parent of {} "
                "because it causes a cyclic parenting."
            ).format(parent.text, self.text)
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
    def key(self):
        """A unique tuple describing the path to this group"""
        self_tuple = (self.section, self.order, self.text)
        if self.parent is None:
            return tuple([self_tuple])
        return tuple([*self.parent.key, self_tuple])

    @property
    def path(self):
        """A list containing the chain of groups that contain this group"""
        if self.parent is None:
            return [self]
        return [*self.parent.path, self]

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################
    # label replaced with text
    @property
    def label(self):
        """Group text.

        **DEPRECATED: renamed as text**

        Returns:
            The button text as a ``str``
        """
        warnings.warn("Group.label has been renamed Group.text", DeprecationWarning)
        return self.text

    @label.setter
    def label(self, label):
        warnings.warn("Group.label has been renamed Group.text", DeprecationWarning)
        self.text = label

    ######################################################################
    # End backwards compatibility.
    ######################################################################


Group.APP = Group("*", order=0)
Group.FILE = Group("File", order=1)
Group.EDIT = Group("Edit", order=10)
Group.VIEW = Group("View", order=20)
Group.COMMANDS = Group("Commands", order=30)
Group.WINDOW = Group("Window", order=90)
Group.HELP = Group("Help", order=100)


class Command:
    """
    Args:
        action: a function to invoke when the command is activated.
        text: caption for the command.
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
            alphabetically by text within its section.
        enabled: whether to enable the command or not.
    """

    def __init__(
        self,
        action,
        text=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
        # can be removed when the handling for
        # `label` is removed
        shortcut=None,
        tooltip=None,
        icon=None,
        group=None,
        section=None,
        order=None,
        enabled=True,
        factory=None,  # DEPRECATED!
        label=None,  # DEPRECATED!
    ):
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################
        # When deleting this block, also delete the NOT_PROVIDED
        # placeholder, and replace its usage in default values.

        # label replaced with text
        if label is not None:
            if text is not NOT_PROVIDED:
                raise ValueError(
                    "Cannot specify both `label` and `text`; "
                    "`label` has been deprecated, use `text`"
                )
            else:
                warnings.warn(
                    "Command.label has been renamed Command.text", DeprecationWarning
                )
                text = label
        elif text is NOT_PROVIDED:
            # This would be raised by Python itself; however, we need to use a placeholder
            # value as part of the migration from text->value.
            raise TypeError(
                "Command.__init__ missing 1 required positional argument: 'text'"
            )

        ##################################################################
        # End backwards compatibility.
        ##################################################################
        orig_action = action
        self.action = wrapped_handler(self, action)
        self.text = text

        self.shortcut = shortcut
        self.tooltip = tooltip
        self.icon = icon

        self.group = group if group else Group.COMMANDS
        self.section = section if section else 0
        self.order = order if order else 0

        self.factory = get_platform_factory()
        self._impl = self.factory.Command(interface=self)

        self.enabled = enabled and orig_action is not None

    @property
    def key(self):
        """A unique tuple describing the path to this command"""
        return tuple([*self.group.key, (self.section, self.order, self.text)])

    def bind(self, factory=None):
        warnings.warn(
            "Commands no longer need to be explicitly bound.", DeprecationWarning
        )
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
        """The Icon for the app.

        :returns: A ``toga.Icon`` instance for the app's icon.
        """
        return self._icon

    @icon.setter
    def icon(self, icon_or_name):
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

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################
    # label replaced with text
    @property
    def label(self):
        """Command text.

        **DEPRECATED: renamed as text**

        Returns:
            The command text as a ``str``
        """
        warnings.warn("Command.label has been renamed Command.text", DeprecationWarning)
        return self.text

    @label.setter
    def label(self, label):
        warnings.warn("Command.label has been renamed Command.text", DeprecationWarning)
        self.text = label

    ######################################################################
    # End backwards compatibility.
    ######################################################################


class Break:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{self.name} break>"


GROUP_BREAK = Break("Group")
SECTION_BREAK = Break("Section")


class CommandSet:
    """

    Args:
        factory:
        widget:
        on_change:

    Todo:
        * Add missing Docstrings.
    """

    def __init__(
        self,
        factory=None,  # DEPRECATED!
        widget=None,
        on_change=None,
    ):
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self.widget = widget
        self._commands = set()
        self.on_change = on_change

    def add(self, *commands):
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
