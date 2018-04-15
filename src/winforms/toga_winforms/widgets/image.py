from toga_winforms.libs import *


class Image(object):
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self

    def load_image(self, path):
        print('[Image.py] Loading image, path: ', path)
        if path.startswith('http://') or path.startswith('https://'):
            print('[Image.py] Temporarily image is the path')
            self.native = path
            print('[Image.py] native is: ', self.native)
        else:
            self.native = WinImage.FromFile(path)
