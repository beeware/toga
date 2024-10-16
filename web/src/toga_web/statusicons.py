import toga


class StatusIcon:
    def __init__(self, interface):
        self.interface = interface
        self.native = None

    def set_icon(self, icon):
        pass

    def create(self):
        toga.NotImplementedWarning.warn("Web", "Status Icons")

    def remove(self):
        pass


class SimpleStatusIcon(StatusIcon):
    pass


class MenuStatusIcon(StatusIcon):
    pass


class StatusIconSet:
    def __init__(self, interface):
        self.interface = interface

    def create(self):
        pass
