from ..libs import NSImage


class Icon:
    EXTENSION = '.icns'

    def __init__(self, interface):
        self.interface = interface
        interface._impl = self
        self.native = None

    def create(self, filename):
        self.native = NSImage.alloc().initWithContentsOfFile(filename)

