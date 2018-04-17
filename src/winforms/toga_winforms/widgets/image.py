from toga_winforms.libs import WinImage


class Image(object):
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self

    def load_image(self, path):
        if path.startswith('http://') or path.startswith('https://'):
            self.native = path
        else:
            self.native = WinImage.FromFile(path)
