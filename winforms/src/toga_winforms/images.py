from toga_winforms.libs import MemoryStream, WinImage


class Image:
    def __init__(self, interface, path=None, url=None, data=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = WinImage.FromFile(str(path))
        elif url:
            # Windows loads URL images in the view,
            # not as standalone resources
            self.native = None
        elif data:
            stream = MemoryStream(data)
            self.native = WinImage.FromStream(stream)

    def save(self, path):
        self.native.Save(str(path))
