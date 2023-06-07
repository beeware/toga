from toga_winforms.libs import MemoryStream, WinImage


class Image:
    def __init__(self, interface, path=None, data=None):
        self.interface = interface

        if path:
            self.native = WinImage.FromFile(str(path))
        else:
            stream = MemoryStream(data)
            self.native = WinImage.FromStream(stream)

    def get_width(self):
        return self.native.Width

    def get_height(self):
        return self.native.Height

    def save(self, path):
        self.native.Save(str(path))
