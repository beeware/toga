from toga_winforms.libs import WinImage


class Image(object):
    def __init__(self, interface, path=None, url=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = WinImage.FromFile(str(path))
        elif url:
            # Windows loads URL images in the view,
            # not as standalone resources
            self.native = None
