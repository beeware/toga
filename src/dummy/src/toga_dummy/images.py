from .utils import LoggedObject


class Image(LoggedObject):
    def __init__(self, interface, path=None, url=None, data=None):
        super().__init__()
        self.interface = interface
        self.path = path
        self.url = url

        if self.path:
            self._action('load image file', path=path)
        elif self.url:
            self._action('load image url', url=url)
        elif data:
            self._action('load image data', data=data)
