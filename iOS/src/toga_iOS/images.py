from toga_iOS.libs import NSData, UIImage


class Image:
    def __init__(self, interface, path=None, url=None, data=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = UIImage.alloc().initWithContentsOfFile(str(path))
        else:
            self.native = UIImage.imageWithData(
                NSData.dataWithBytes(data, length=len(data))
            )

    def get_width(self):
        return self.native.size.width

    def get_height(self):
        return self.native.size.height

    def save(self, path):
        self.interface.factory.not_implemented("Image.save()")
