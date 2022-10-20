from toga_iOS.libs import UIImage


class Icon:
    EXTENSIONS = ['.icns', '.png', '.bmp', '.ico']
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface

        self.native = UIImage.alloc().initWithContentsOfFile(str(path))
