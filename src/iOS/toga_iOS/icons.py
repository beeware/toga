from toga_iOS.libs import UIImage


class Icon:
    def __init__(self, interface, path):
        self.interface = interface

        self.native = UIImage.alloc().initWithContentsOfFile(str(path))
