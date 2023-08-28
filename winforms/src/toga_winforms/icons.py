from System import ArgumentException
from System.Drawing import Bitmap, Icon as WinIcon


class Icon:
    EXTENSIONS = [".ico", ".png", ".bmp"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.path = path

        try:
            if path.suffix == ".ico":
                self.native = WinIcon(str(path))
            else:
                icon_bitmap = Bitmap(str(path))
                icon_handle = icon_bitmap.GetHicon()
                self.native = WinIcon.FromHandle(icon_handle)
        except ArgumentException:
            raise ValueError(f"Unable to load icon from {path}")
