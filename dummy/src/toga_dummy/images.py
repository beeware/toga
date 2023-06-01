from .utils import LoggedObject, not_required


@not_required  # Testbed coverage is complete
class Image(LoggedObject):
    def __init__(self, interface, path=None, url=None, data=None):
        super().__init__()
        self.interface = interface
        self.path = path
        self.url = url

        if self.path:
            self._action("load image file", path=path)
        elif self.url:
            self._action("load image url", url=url)
        elif data:
            self._action("load image data", data=data)

    def get_width(self):
        return 37

    def get_height(self):
        return 42

    def save(self, path):
        self._action("save", path=path)
