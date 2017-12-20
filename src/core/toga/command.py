from toga.handlers import wrapped_handler


class Group:
    """

    Args:
        label:
        order:
    """
    def __init__(self, label, order=None):
        self.label = label
        self.order = order if order else 0

    def __lt__(self, other):
        return (
            self.order < other.order
            or self.order == other.order and self.label < other.label
        )

    def __eq__(self, other):
        return self.order == other.order and self.label == other.label


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
            shortcut: (optional) a key combination that can be used to invoke the command.
            tooltip: (optional) a short description for what the command will do.
            icon: (optional) a path to an icon resource to decorate the command.
            group: (optional) a Group object describing a collection of similar commands. If no group is specified, a default "Command" group will be used.
            section: (optional) an integer providing a sub-grouping. If no section is specified, the command will be allocated to section 0 within the group.
            order: (optional) an integer indicating where a command falls within a section. If a Command doesn't have an order, it will be sorted alphabetically by label within its section.
    """
    def __init__(self, action, label,
                 shortcut=None, tooltip=None, icon=None,
                 group=None, section=None, order=None, factory=None):
        self.action = wrapped_handler(self, action)
        self.label = label

        self.shortcut = shortcut
        self.tooltip = tooltip
        self.icon_id = icon

        self.group = group if group else Group.COMMANDS
        self.section = section if section else 0
        self.order = order if order else 0

        self._enabled = self.action is not None

        self._widgets = []
        self._impl = None

    def bind(self, factory):
        if self._impl is None:
            self._impl = factory.Command(interface=self)
        return self._impl

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        for widget in self._widgets:
            widget.enabled = value


GROUP_BREAK = object()
SECTION_BREAK = object()


def cmd_sort_key(value):
    return (value.group, value.section, value.order, value.label)


class CommandSet:
    """

    Args:
        widget:
        on_change:

    Todo:
        * Add missing Docstrings.
    """
    def __init__(self, widget, on_change=None):

        self.widget = widget
        self._values = set()
        self.on_change = on_change

    def add(self, *values):
        if self.widget and self.widget.app != None:
            self.widget.app.commands.add(*values)
        self._values.update(values)
        if self.on_change:
            self.on_change()

    def __iter__(self):
        prev_cmd = None
        for cmd in sorted(self._values, key=cmd_sort_key):
            if prev_cmd:
                if cmd.group != prev_cmd.group:
                    yield GROUP_BREAK
                elif cmd.section != prev_cmd.section:
                    yield SECTION_BREAK

            yield cmd
            prev_cmd = cmd
