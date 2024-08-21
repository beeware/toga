from .utils import LoggedObject


class StatusIcon(LoggedObject):
    def __init__(self, interface):
        self.interface = interface

    def set_icon(self, icon):
        self._action("set icon", icon=icon)

    def create(self):
        self._action("create")
        self.set_icon(self.interface.icon)

    def remove(self):
        self._action("remove")


class SimpleStatusIcon(StatusIcon):
    def simulate_press(self):
        self.interface.on_press()


class MenuStatusIcon(StatusIcon):
    pass


class StatusIconSet(LoggedObject):
    def __init__(self, interface):
        self.interface = interface

    def create(self):
        self._action("create status icons")
