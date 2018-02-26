import os
from toga_iOS.libs import(
    NSData,
    NSURL,
    UIImage
)


class Image(object):
    def __init__(self, interface):
        self.interface = interface

    def load_image(self, path):
        if path.startswith('http://') or path.startswith('https://'):
            self.native = UIImage.imageWithData_(NSData.dataWithContentsOfURL_(NSURL.URLWithString_(path)))
        else:
            self.native = UIImage.imageNamed_(os.path.basename(path))
