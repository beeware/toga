from toga.interface.command import Group, Command as BaseCommand

from .widgets.icon import Icon


class Command(BaseCommand):
    def __init__(self, action, label,
                         shortcut=None, tooltip=None, icon=None,
                         group=None, section=None, order=None):
        super().__init__(action, label=label,
                         shortcut=shortcut, tooltip=tooltip, icon=icon,
                         group=group, section=section, order=order)

        if self.icon_id:
            self.icon = Icon.load(self.icon_id)
        else:
            self.icon = None

        self._widgets = []

    def _set_enabled(self, value):
        for widget in self._widgets:
            widget.setEnabled_(value)
