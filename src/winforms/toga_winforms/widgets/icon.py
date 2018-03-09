import os

from toga_winforms.libs import WinIcon, Bitmap


class Icon:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        valid_icon_extensions = ('.png', '.bmp', '.ico')
        file_path, file_extension = os.path.splitext(self.interface.filename)

        if file_extension == '.ico':
            self.native = WinIcon(self.interface.filename)

        elif os.path.isfile(file_path + '.ico'):
            self.native = WinIcon(file_path + '.ico')

        elif file_extension in valid_icon_extensions:

            icon_bitmap = Bitmap(self.interface.filename)
            icon_handle = icon_bitmap.GetHicon()
            self.native = WinIcon.FromHandle(icon_handle)

        else:
            raise AttributeError("No valid icon format for winforms")
