from toga_cocoa.libs import NSURL, NSImage
from toga_cocoa.libs.foundation import NSData


class Image:
    def __init__(self, interface, path=None, url=None, data=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = NSImage.alloc().initWithContentsOfFile(str(path))
        elif url:
            self.native = NSImage.alloc().initByReferencingURL(
                NSURL.URLWithString_(url)
            )
        elif data:
            self.native = NSImage.alloc().initWithData(
                NSData.dataWithBytes(data, length=len(data))
            )
