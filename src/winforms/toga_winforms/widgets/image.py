from toga_winforms.libs import WinImage
import os

class Image(object):
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self

    def load_image(self, path):
        if path.startswith('http://') or path.startswith('https://'):
            self.native = path
        else:
            if os.path.isfile(path):
                self.native = WinImage.FromFile(path)
            else:
                raise ValueError("No image file available at ", path)
