from toga import Icon


class Command():
    def __init__(self, interface):
        self.interface = interface


        if self.interface.icon_id:
            self.icon = Icon.load(self.interface.icon_id)
        else:
            self.icon = None

        self._widgets = []

    def _set_enabled(self, value):
        for widget in self.interface._widgets:
            try:
                widget.set_sensitive(value)
            except AttributeError:
                widget.set_enabled(value)
