import toga

# Not implemented on Qt yet.


class StatusIcon:
    def __init__(self, interface):
        self.interface = interface
        self.native = None

    def set_icon(self, icon):
        pass

    def create(self):
        toga.NotImplementedWarning.warn("Qt", "Status Icons")

    # Remove no-cover when this is implemented
    def remove(self):  # pragma: no cover
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
