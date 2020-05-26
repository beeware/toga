
class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []

    def set_enabled(self, value):
        for widget in self.native:
            widget.enabled = value
