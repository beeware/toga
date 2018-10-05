import os

from toga import Icon as toga_Icon

from .libs import Bitmap, WinIcon


class Icon:
    def __init__(self, interface):

        def create_icon_from_file(filename):
            icon_bitmap = Bitmap(self.interface.filename)
            icon_handle = icon_bitmap.GetHicon()
            return WinIcon.FromHandle(icon_handle)

        self.interface = interface
        self.interface._impl = self
        valid_icon_extensions = ('.png', '.bmp', '.ico')
        file_path, file_extension = os.path.splitext(self.interface.filename)

        if file_extension == '.ico':
            self.native = WinIcon(self.interface.filename)

        elif os.path.isfile(file_path + '.ico'):
            self.native = WinIcon(file_path + '.ico')

        elif file_extension in valid_icon_extensions:
            self.native = create_icon_from_file(self.interface.filename)

        elif os.path.isfile(file_path + '.png'):
            self.native = create_icon_from_file(file_path + '.png')

        elif os.path.isfile(file_path + '.bmp'):
            self.native = create_icon_from_file(file_path + '.bmp')

        else:
            print("[Winforms] No valid icon format available for {}; "
                  "fall back on Tiberius instead".format(
                self.interface.filename))
            tiberius_file = toga_Icon.TIBERIUS_ICON.filename + '.ico'
            self.interface.icon = toga_Icon.TIBERIUS_ICON
            self.native = WinIcon(tiberius_file)
