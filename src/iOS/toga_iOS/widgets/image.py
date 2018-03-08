import os
import toga
from toga_iOS.libs import(
    NSData,
    NSURL,
    UIImage
)

class Image(object):
    def __init__(self, interface):
        self.interface = interface

    def __get_full_path(self, path):
        if (os.path.isabs(path)):
            return path
        else:
            return os.path.join(toga.App.app_dir, path)
    
    def load_image(self, path):
        # If a remote URL is provided, use the download from NSData (similar to toga-cocoa)
        if path.startswith('http://') or path.startswith('https://'):
            self.native = UIImage.imageWithData_(NSData.dataWithContentsOfURL_(NSURL.URLWithString_(path)))
        else:
            basename = os.path.basename(path)
            if basename == path:
                # if a path isn't provided, assume that the image is bundled into the app
                self.native = UIImage.imageNamed_(basename)
            else:
                # load with the full path
                self.native = UIImage.alloc().initWithContentsOfFile_(self.__get_full_path(path))
