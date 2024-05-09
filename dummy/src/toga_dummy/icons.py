from .utils import LoggedObject


class Icon(LoggedObject):
    ICON_FAILURE = None
    EXTENSIONS = [".png", ".ico"]
    SIZES = None

    def __init__(self, interface, path):
        super().__init__()
        self.interface = interface
        if self.ICON_FAILURE:
            raise self.ICON_FAILURE
        else:
            if path is None:
                self.path = "<APP ICON>"
            elif path == {}:
                raise FileNotFoundError("No image variants found")
            else:
                self.path = path
