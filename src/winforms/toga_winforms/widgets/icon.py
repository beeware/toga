from toga_winforms.libs import WinIcon
import os


class Icon:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.native = WinIcon(self.interface.filename)
