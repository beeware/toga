from .base import Widget
from ..platform import get_platform_factory


class Image(object):
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
