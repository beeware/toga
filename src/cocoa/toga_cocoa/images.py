from toga_cocoa.libs import NSImage, NSURL,NSData


class Image:
    def __init__(self, interface, path=None, url=None, data=None,image=None):
        self.interface = interface
        self.path = path
        self.url = url
        self.data = data
        self.image=image

        if path:
            self.native = NSImage.alloc().initWithContentsOfFile(str(path))
        elif url:
            self.native = NSImage.alloc().initByReferencingURL(
                NSURL.URLWithString_(url))
        elif data:
            self.native = NSImage.alloc().initWithData(data)
        elif image:
            self.native = NSImage(image)
            
            
