import toga


class BaseStatusIcon:
    def __init__(self, interface):
        self.interface = interface
        self.native = None

    def set_icon(self, icon):
        pass

    def create(self):
        toga.NotImplementedWarning.warn("Textual", "Status Icons")

    def remove(self):
        pass


class StatusIcon(BaseStatusIcon):
    pass


class MenuStatusIcon(BaseStatusIcon):
    pass


class StatusIconSet:
    def __init__(self, interface):
        self.interface = interface

    def create(self):
        pass
