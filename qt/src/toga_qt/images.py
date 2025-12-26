from pathlib import Path

from PySide6.QtCore import QBuffer, QIODevice
from PySide6.QtGui import QImage

from toga.images import ImageLoadError

from .libs import create_qapplication


class Image:
    RAW_TYPE = QImage

    def __init__(self, interface, data=None, raw=None):
        # A QApplication must exist before pixmaps can be manipulated
        create_qapplication()

        self.interface = interface

        if data:
            image = QImage()
            if not image.loadFromData(data):
                raise ImageLoadError
            self.native = image
        else:
            self.native = raw

    def get_width(self):
        return self.native.width()

    def get_height(self):
        return self.native.height()

    def get_data(self):
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        if not self.native.save(buffer, "PNG"):  # pragma: no cover
            raise ValueError("Unable to get PNG data for image")
        return buffer.data().data()

    def save(self, path):
        path = Path(path)
        filetype = {
            ".jpg": "JPEG",
            ".jpeg": "JPEG",
            ".png": "PNG",
            ".bmp": "BMP",
        }.get(path.suffix.lower())

        if not filetype:
            raise ValueError(f"Don't know how to save image of type {path.suffix!r}")

        if not self.native.save(str(path), filetype):  # pragma: no cover
            raise ValueError(f"Failed to save image to {path}")
