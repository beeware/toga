from .libs import Bitmap, WinIcon


class Icon:
    EXTENSIONS = ['.ico', '.png', '.bmp']
    SIZES = None

    def __init__(self, interface, file_path):
        self.interface = interface
        self.interface._impl = self

        if file_path.suffix == '.ico':
            self.native = WinIcon(str(file_path))
        else:
            icon_bitmap = Bitmap(str(file_path))
            icon_handle = icon_bitmap.GetHicon()
            self.native = WinIcon.FromHandle(icon_handle)
