from .utils import LoggedObject


class Font(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self

    def measure(self, text, tight):
        self._action('measure', text=text, tight=tight)
