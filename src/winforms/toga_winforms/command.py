from toga.icons import Icon as CoreIcon


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []
        if self.interface.icon_id:
            # If icon_id is an icon, not a filepath
            if type(self.interface.icon_id) is not str:
                self.interface.icon = self.interface.icon_id
            else:
                self.interface.icon = CoreIcon(self.interface.icon_id)
        else:
            self.interface.icon = None

    def set_enabled(self, value):
        if self.native:
            for widget in self.native:
                widget.Enabled = self.interface.enabled

    def as_handler(self):
        def handler(sender, event):
            return self.interface.action(None)

        return handler
