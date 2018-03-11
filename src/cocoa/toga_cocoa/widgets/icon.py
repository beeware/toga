import os

from toga import Icon as toga_Icon
from toga_cocoa.libs import NSImage


class Icon:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        file_path, file_extension = os.path.splitext(self.interface.filename)
        valid_icon_extensions = ('.png', '.bmp', '.ico')

        if file_extension == '.icns':
            self.native = NSImage.alloc().initWithContentsOfFile(self.interface.filename)
        elif os.path.isfile(file_path + '.icns'):
            self.native = NSImage.alloc().initWithContentsOfFile(file_path + '.icns')
        elif file_extension in valid_icon_extensions:
            self.native = NSImage.alloc().initWithContentsOfFile(self.interface.filename)
        elif os.path.isfile(file_path + '.png'):
            self.native = NSImage.alloc().initWithContentsOfFile(file_path + '.png')
        elif os.path.isfile(file_path + '.bmp'):
            self.native = NSImage.alloc().initWithContentsOfFile(file_path + '.bmp')
        else:
            print("[Cocoa] No valid icon format available for {}; "
                  "fall back on Tiberius instead".format(
                self.interface.filename))
            tiberius_file = toga_Icon.TIBERIUS_ICON.filename + '.icns'
            self.interface.icon = toga_Icon.TIBERIUS_ICON
            self.native = NSImage.alloc().initWithContentsOfFile(tiberius_file)
