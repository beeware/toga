from .utils import LoggedObject


class Icon(LoggedObject):
    EXTENSIONS = [".png", ".ico"]
    SIZES = None

    def __init__(self, interface, path):
        super().__init__()
        self.interface = interface
        self.path = path
        if path == {}:
            raise FileNotFoundError("No image variants found")
