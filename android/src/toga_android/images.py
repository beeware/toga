from pathlib import Path

from android.graphics import Bitmap, BitmapFactory
from java.io import ByteArrayOutputStream, FileOutputStream


class Image:
    RAW_TYPE = Bitmap

    def __init__(self, interface, path=None, data=None, raw=None):
        self.interface = interface

        if path:
            self.native = BitmapFactory.decodeFile(str(path))
            if self.native is None:
                raise ValueError(f"Unable to load image from {path}")
        elif data:
            self.native = BitmapFactory.decodeByteArray(data, 0, len(data))
            if self.native is None:
                raise ValueError("Unable to load image from data")
        else:
            self.native = raw

    def get_width(self):
        return self.native.getWidth()

    def get_height(self):
        return self.native.getHeight()

    def get_data(self):
        stream = ByteArrayOutputStream()
        self.native.compress(Bitmap.CompressFormat.PNG, 90, stream)
        return bytes(stream.toByteArray())

    def save(self, path):
        path = Path(path)
        try:
            format = {
                ".jpg": Bitmap.CompressFormat.JPEG,
                ".jpeg": Bitmap.CompressFormat.JPEG,
                ".png": Bitmap.CompressFormat.PNG,
            }[path.suffix.lower()]
            str_path = str(path)
        except KeyError:
            raise ValueError(f"Don't know how to save image of type {path.suffix!r}")

        out = FileOutputStream(str_path)
        self.native.compress(format, 90, out)
        out.flush()
        out.close()
