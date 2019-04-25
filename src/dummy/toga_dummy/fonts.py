from .utils import LoggedObject


class Font(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def measure(self, text, tight=False):
        self._action('measure', text=text, tight=tight)
