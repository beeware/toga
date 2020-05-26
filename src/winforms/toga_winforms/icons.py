from .libs import Bitmap, WinIcon


class Icon:
    EXTENSIONS = ['.ico', '.png', '.bmp']
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.path = path

        if path.suffix == '.ico':
            self.native = WinIcon(str(path))
        else:
            icon_bitmap = Bitmap(str(path))
            icon_handle = icon_bitmap.GetHicon()
            self.native = WinIcon.FromHandle(icon_handle)
