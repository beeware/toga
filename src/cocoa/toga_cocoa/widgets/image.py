from toga_cocoa.libs import *


class Image(object):
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self

    def load_image(self, path):
        if path.startswith('http://') or path.startswith('https://'):
            self.native = NSImage.alloc().initByReferencingURL(NSURL.URLWithString_(path))
        else:
            self.native = NSImage.alloc().initWithContentsOfFile(path)
