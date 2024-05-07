import sys

from System import ArgumentException
from System.Drawing import Bitmap, Icon as WinIcon


class Icon:
    EXTENSIONS = [".ico", ".png", ".bmp"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.path = path

        try:
            if path is None:
                self.native = WinIcon.ExtractAssociatedIcon(sys.executable)
                self.bitmap = Bitmap.FromHicon(self.native.Handle)
            elif path.suffix == ".ico":
                self.native = WinIcon(str(path))
                self.bitmap = Bitmap.FromHicon(self.native.Handle)
            else:
                self.bitmap = Bitmap(str(path))
                self.native = WinIcon.FromHandle(self.bitmap.GetHicon())
        except ArgumentException:
            raise ValueError(f"Unable to load icon from {path}")
