from toga.icons import Icon


class Command:
    def __init__(self, interface):
        self.interface = interface

        if self.interface.icon_id:
            self.icon = Icon.load(self.interface.icon_id)
        else:
            self.icon = None
