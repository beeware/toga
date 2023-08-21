from pathlib import Path

from System import (
    ArgumentException,
    OutOfMemoryException,
)
from System.Drawing import Image as WinImage
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream


class Image:
    def __init__(self, interface, path=None, data=None):
        self.interface = interface

        if path:
            try:
                self.native = WinImage.FromFile(str(path))
            except OutOfMemoryException:
                # OutOfMemoryException is what Winforms raises when a file
                # isn't a valid image file.
                raise ValueError(f"Unable to load image from {path}")
        else:
            try:
                stream = MemoryStream(data)
                self.native = WinImage.FromStream(stream)
            except ArgumentException:
                raise ValueError("Unable to load image from data")

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
