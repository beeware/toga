# from toga.interface.command import Group, Command as BaseCommand

from toga.widgets.icon import Icon


class Command():
    def __init__(self, interface):
        self.interface = interface

        if self.interface.icon_id:
            self.icon = Icon.load(self.interface.icon_id)
        else:
            self.icon = None

        self._widgets = []

    def _set_enabled(self, value):
        for widget in self._widgets:
            widget.setEnabled_(value)