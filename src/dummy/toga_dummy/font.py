from .utils import LoggedObject


class Font(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def create_string(self, text):
        self._action('create string', text=text)

    def measure(self, text, tight=False):
        self._action('measure', text=text, tight=tight)
