from ..utils import LoggedObject


class Image(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self

    def load_image(self, path):
        self._action('load image', path=path)
