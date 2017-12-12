from toga.platform import get_platform_factory


class Image(object):
    """

    Args:
        path (str): Path to the image.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """
    def __init__(self, path, factory=None):
        self.factory = factory if factory else get_platform_factory()
        self._impl = self.factory.Image(interface=self)
        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path
        self._impl.load_image(self._path)
