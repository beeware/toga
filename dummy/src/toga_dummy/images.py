from .utils import LoggedObject, not_required


@not_required  # Testbed coverage is complete
class Image(LoggedObject):
    def __init__(self, interface, path=None, data=None):
        super().__init__()
        self.interface = interface
        if path:
            self._action("load image file", path=path)
        else:
            self._action("load image data", data=data)

    def get_width(self):
        return 60

    def get_height(self):
        return 40

    def save(self, path):
        self._action("save", path=path)
