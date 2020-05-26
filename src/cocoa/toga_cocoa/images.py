from toga_cocoa.libs import NSImage, NSURL


class Image:
    def __init__(self, interface, path=None, url=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = NSImage.alloc().initWithContentsOfFile(str(path))
        elif url:
            self.native = NSImage.alloc().initByReferencingURL(
                NSURL.URLWithString_(url)
            )
