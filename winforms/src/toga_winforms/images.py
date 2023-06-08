from pathlib import Path

from toga_winforms.libs import ImageFormat, MemoryStream, WinImage


class Image:
    def __init__(self, interface, path=None, data=None):
        self.interface = interface

        if path:
            self.native = WinImage.FromFile(str(path))
        else:
            stream = MemoryStream(data)
            self.native = WinImage.FromStream(stream)

    def get_width(self):
        return self.native.Width

    def get_height(self):
        return self.native.Height

    def save(self, path):
        path = Path(path)
        try:
            filetype = {
                ".jpg": ImageFormat.Jpeg,
                ".jpeg": ImageFormat.Jpeg,
                ".png": ImageFormat.Png,
                ".gif": ImageFormat.Gif,
                ".bmp": ImageFormat.Bmp,
                ".tiff": ImageFormat.Tiff,
            }[path.suffix.lower()]
            str_path = str(path)
        except KeyError:
            raise ValueError(f"Don't know how to save image of type {path.suffix!r}")

        self.native.Save(str_path, filetype)
