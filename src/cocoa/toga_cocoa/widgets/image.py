import os

import toga
from toga_cocoa.libs import *


class Image(object):
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self

    def __get_full_path(self, path):
        if path.startswith(('http://', 'https://')) or os.path.isabs(path):
            return path
        else:
            return os.path.join(toga.App.app_dir, path)

    def load_image(self, path):
        if path.startswith(('http://', 'https://')):
            self.native = NSImage.alloc().initByReferencingURL(NSURL.URLWithString_(path))
        else:
            self.native = NSImage.alloc().initWithContentsOfFile(self.__get_full_path(path))
