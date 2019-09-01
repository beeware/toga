from toga_dummy.utils import LoggedObject


class Command(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def set_enabled(self, value):
        self._action('set enabled', value=value)
