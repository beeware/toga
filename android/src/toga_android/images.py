from pathlib import Path

from java.io import FileOutputStream

from android.graphics import Bitmap, BitmapFactory


class Image:
    def __init__(self, interface, path=None, data=None):
        self.interface = interface

        if path:
            self.native = BitmapFactory.decodeFile(str(path))
            if self.native is None:
                raise ValueError(f"Unable to load image from {path}")
        else:
            self.native = BitmapFactory.decodeByteArray(data, 0, len(data))
            if self.native is None:
                raise ValueError("Unable to load image from data")

    def get_width(self):
        return self.native.getWidth()

    def get_height(self):
        return self.native.getHeight()

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
