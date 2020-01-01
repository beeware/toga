from toga_iOS.libs import UIImage


class Icon:
    def __init__(self, interface, file_path):
        self.interface = interface
        self.interface._impl = self

        self.native = UIImage.alloc().initWithContentsOfFile(str(file_path))
