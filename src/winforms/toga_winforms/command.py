
class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []

    def set_enabled(self, value):
        if self.native:
            for widget in self.native:
                widget.Enabled = self.interface.enabled

    def as_handler(self):
        def handler(sender, event):
            return self.interface.action(None)

        return handler
