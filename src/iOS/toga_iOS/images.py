import os

import toga
from toga_iOS.libs import NSURL, NSData, UIImage


class Image(object):
    def __init__(self, interface):
        self.interface = interface

    @staticmethod
    def _get_full_path(path):
        if path.startswith(('http://', 'https://')) or os.path.isabs(path):
            return path
        else:
            return os.path.join(toga.App.app_dir, path)

    def load_image(self, path):
        # If a remote URL is provided, use the download from NSData (similar to toga-cocoa)
        if path.startswith('http://') or path.startswith('https://'):
            self.native = UIImage.imageWithData_(NSData.dataWithContentsOfURL_(NSURL.URLWithString_(path)))
        else:
            self.native = UIImage.alloc().initWithContentsOfFile_(self._get_full_path(path))
