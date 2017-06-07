
class Group:
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
    def __init__(self, action, label,
                 shortcut=None, tooltip=None, icon=None,
                 group=None, section=None, order=None):
        self.action = action
        self.label = label

        self.shortcut = shortcut
        self.tooltip = tooltip
        self.icon_id = icon

        self.group = group if group else Group.COMMANDS
        self.section = section if section else 0
        self.order = order if order else 0

        self._enabled = self.action is not None

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        self._set_enabled(value)

    def _set_enabled(self, value):
        pass


GROUP_BREAK = object()
SECTION_BREAK = object()


def cmd_sort_key(value):
    return (value.group, value.section, value.order, value.label)


class CommandSet:
    def __init__(self, widget, on_change=None):
        self.widget = widget
        self._values = set()
        self.on_change = on_change

    def add(self, *values):
        if self.widget:
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
