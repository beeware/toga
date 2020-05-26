from toga_cocoa.libs import NSImage


class Icon:
    EXTENSIONS = ['.icns', '.png', '.pdf']
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.interface._impl = self
        self.path = path

        self.native = NSImage.alloc().initWithContentsOfFile(str(path))
