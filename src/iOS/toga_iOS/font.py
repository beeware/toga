from .libs import UIFont


class Font:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        self.native = UIFont.fontWithName_size_(self.family, self.size)
