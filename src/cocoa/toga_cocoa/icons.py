from toga_cocoa.libs import NSImage


class Icon:
    EXTENSIONS = ['.icns', '.png', '.bmp', '.ico']
    SIZES = None

    def __init__(self, interface, file_path):
        self.interface = interface
        self.interface._impl = self

        self.native = NSImage.alloc().initWithContentsOfFile(str(file_path))
