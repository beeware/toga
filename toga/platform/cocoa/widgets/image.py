import os

from ..libs import *


class Image(object):
    def __init__(self, path, system=False):
        self.path = path
        self.system = system

        if self.system:
            filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'resources', self.path)
        else:
            filename = self.path

        self._impl = NSImage.alloc().initWithContentsOfFile_(get_NSString(filename))


TIBERIUS_ICON = Image('tiberius.icns', system=True)
