from toga_cocoa.libs import NSImage
import os


class Icon:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.native = NSImage.alloc().initWithContentsOfFile(interface.filename)

        valid_icon_extensions = ('.png', '.bmp', '.icns')
        file_path, file_extension = os.path.splitext(self.interface.filename)

        if file_extension in valid_icon_extensions:
            self.native = NSImage.alloc().initWithContentsOfFile(interface.filename)

        elif os.path.isfile(file_path + '.icns'):
            self.native = NSImage.alloc().initWithContentsOfFile(file_path + '.icns')

        else:
            raise AttributeError("No valid icon format for cocoa")
