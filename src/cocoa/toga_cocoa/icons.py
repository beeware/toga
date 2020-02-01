from toga_cocoa.libs import NSImage


class Icon:
    EXTENSIONS = ['.icns', '.tiff', '.png', '.jpeg', '.bmp', '.ico', '.pdf', '.eps', '.psd']
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.interface._impl = self
        self.path = path

        self.native = NSImage.alloc().initWithContentsOfFile(str(path))
