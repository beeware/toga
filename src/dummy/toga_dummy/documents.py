from .utils import LoggedObject


class Document(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
