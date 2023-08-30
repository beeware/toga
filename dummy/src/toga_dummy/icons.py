from .utils import LoggedObject, not_required


@not_required  # Testbed coverage is complete.
class Icon(LoggedObject):
    EXTENSIONS = [".png", ".ico"]
    SIZES = None

    def __init__(self, interface, path):
        super().__init__()
        self.interface = interface
        self.path = path
