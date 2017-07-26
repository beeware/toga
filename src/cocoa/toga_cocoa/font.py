from .libs import NSFont


class Font():
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        self.native = NSFont.fontWithName_size_(self.interface.family, self.interface.size)
