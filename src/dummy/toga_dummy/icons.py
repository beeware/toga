from .utils import LoggedObject


class Icon(LoggedObject):
    EXTENSIONS = ['.png', '.ico']
    SIZES = None

    def __init__(self, interface, file_path):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
