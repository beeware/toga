from toga.interface import Font as FontInterface
from .libs import UIFont


class Font(FontInterface):

    def create(self):
        self._impl = UIFont.fontWithName_size_(self.family, self.size)
