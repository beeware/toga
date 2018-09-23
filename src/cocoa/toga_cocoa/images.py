import os

import toga
from toga_cocoa.libs import NSImage, NSURL


class Image(object):
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self

    @staticmethod
    def _get_full_path(path):
        if path.startswith(('http://', 'https://')) or os.path.isabs(path):
            return path
        else:
            return os.path.join(toga.App.app_dir, path)

    def load_image(self, path):
        if path.startswith(('http://', 'https://')):
            self.native = NSImage.alloc().initByReferencingURL(NSURL.URLWithString_(path))
        else:
            self.native = NSImage.alloc().initWithContentsOfFile(self._get_full_path(path))
