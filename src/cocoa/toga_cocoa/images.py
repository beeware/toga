import os

import toga
from toga_cocoa.libs import NSImage, NSURL


class Image:
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self

    def load_image(self, path):
        if path.startswith(('http://', 'https://')):
            self.native = NSImage.alloc().initByReferencingURL(
                NSURL.URLWithString_(path)
            )
        else:
            if os.path.isabs(path):
                filename = str(path)
            else:
                filename = str(self._get_full_path(path))

            self.native = NSImage.alloc().initWithContentsOfFile(filename)
