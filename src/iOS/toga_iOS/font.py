from .libs import UIFont


class Font():

    def create(self):
        self.native = UIFont.fontWithName_size_(self.family, self.size)
