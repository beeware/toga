from pathlib import Path

from toga_iOS.libs import (
    NSData,
    UIImage,
    uikit,
)


class Image:
    def __init__(self, interface, path=None, data=None):
        self.interface = interface

        if path:
            self.native = UIImage.imageWithContentsOfFile(str(path))
            if self.native is None:
                raise ValueError(f"Unable to load image from {path}")
        else:
            self.native = UIImage.imageWithData(
                NSData.dataWithBytes(data, length=len(data))
            )
            if self.native is None:
                raise ValueError("Unable to load image from data")
        self.native.retain()

    def __del__(self):
        if self.native:
            self.native.release()

    def get_width(self):
        return self.native.size.width

    def get_height(self):
        return self.native.size.height

    def save(self, path):
        path = Path(path)
        try:
            converter = {
                ".jpg": uikit.UIImageJPEGRepresentation,
                ".jpeg": uikit.UIImageJPEGRepresentation,
                ".png": uikit.UIImagePNGRepresentation,
            }[path.suffix.lower()]
            str_path = str(path)
        except KeyError:
            raise ValueError(f"Don't know how to save image of type {path.suffix!r}")

        data = converter(self.native)

        NSData(data).writeToFile(str_path, atomically=True)
