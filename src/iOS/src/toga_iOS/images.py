from toga_iOS.libs import NSURL, NSData, UIImage


class Image(object):
    def __init__(self, interface, path=None, url=None, data=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = UIImage.alloc().initWithContentsOfFile_(str(path))
        elif url:
            # If a remote URL is provided, use the download from NSData
            self.native = UIImage.imageWithData_(
                NSData.dataWithContentsOfURL_(
                    NSURL.URLWithString_(path)
                )
            )
        elif data:
            self.native = UIImage.imageWithData_(
                NSData.dataWithBytes(data, length=len(data))
            )
