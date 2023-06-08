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
            self.native = UIImage.alloc().initWithContentsOfFile(str(path))
        else:
            self.native = UIImage.imageWithData(
                NSData.dataWithBytes(data, length=len(data))
            )

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
