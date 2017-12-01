from toga_iOS.libs import UIImage


class Icon:
    def __init__(self, interface):
        self.interface = interface
        interface.__impl = self

        self.native = UIImage.alloc().initWithContentsOfFile(interface.filename)
