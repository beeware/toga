from toga_cocoa.libs import NSImage
import os

class Icon:
    def __init__(self, interface):
        self.interface = interface
        interface._impl = self
        valid_icon_extensions = ('.png', '.bmp', '.icns')
        file_path, file_extension = os.path.splitext(self.interface.filename)

        if file_extension in valid_icon_extensions:
            self.native = NSImage.alloc().initWithContentsOfFile(interface.filename)
        else:
            # Return tiberius?
            raise AttributeError("No valid icon format for cocoa")
