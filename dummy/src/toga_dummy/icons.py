from .utils import LoggedObject


class Icon(LoggedObject):
    ICON_EXISTS = True
    EXTENSIONS = [".png", ".ico"]
    SIZES = None

    def __init__(self, interface, path):
        super().__init__()
        self.interface = interface
        if not self.ICON_EXISTS:
            raise FileNotFoundError("Couldn't find icon")
        elif path is None:
            self.path = "<APP ICON>"
        elif path == {}:
            raise FileNotFoundError("No image variants found")
        else:
            self.path = path
