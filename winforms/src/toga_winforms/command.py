class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []

    def set_enabled(self, value):
        if self.native:
            for widget in self.native:
                widget.Enabled = self.interface.enabled

    def winforms_handler(self, sender, event):
        return self.interface.action(None)
