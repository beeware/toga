from .utils import LoggedObject


class Font(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
