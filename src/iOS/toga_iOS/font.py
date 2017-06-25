from .libs import UIFont


class Font():

    def create(self):
        self._native = UIFont.fontWithName_size_(self.family, self.size)
