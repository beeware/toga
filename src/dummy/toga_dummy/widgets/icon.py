from ..utils import LoggedObject


class Icon(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
