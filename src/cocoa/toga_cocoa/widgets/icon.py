import os

import toga

from ..libs import *


class Icon(object):
    app_icon = None

    def __init__(self, path, system=False):
        self.path = path
        self.system = system

        if self.system:
            filename = os.path.join(os.path.dirname(toga.__file__), 'resources', self.path)
        else:
            filename = self.path

        self._impl = NSImage.alloc().initWithContentsOfFile_(filename)

    @staticmethod
    def load(path_or_icon, default=None):
        if path_or_icon:
            if isinstance(path_or_icon, Icon):
                obj = path_or_icon
            else:
                obj = Icon(path_or_icon)
        elif default:
            obj = default
        return obj


TIBERIUS_ICON = Icon('tiberius.icns', system=True)
