from pathlib import Path

from System import (
    ArgumentException,
)
from System.Drawing import Image as WinImage
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream

from toga.images import ImageLoadError


class Image:
    RAW_TYPE = WinImage

    def __init__(self, interface, data=None, raw=None):
        self.interface = interface

        if data:
            try:
                stream = MemoryStream(data)
                self.native = WinImage.FromStream(stream)
            except ArgumentException as exc:
                raise ImageLoadError from exc
        else:
            self.native = raw

    def get_width(self):
        return self.native.Width

    def get_height(self):
        return self.native.Height

    def get_data(self):
        stream = MemoryStream()
        self.native.Save(stream, ImageFormat.Png)
        return bytes(stream.ToArray())

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
        except KeyError as exc:
            raise ValueError(
                f"Don't know how to save image of type {path.suffix!r}"
            ) from exc

        self.native.Save(str_path, filetype)
