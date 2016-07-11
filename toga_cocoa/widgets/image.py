from ..libs import *


class Image(object):
    def __init__(self, path):
        self.path = path

        if path.startswith('http://') or path.startswith('https://'):
            self._impl = NSImage.alloc().initByReferencingURL_(NSURL.URLWithString_(self.path))
        else:
            self._impl = NSImage.alloc().initWithContentsOfFile_(self.path)
