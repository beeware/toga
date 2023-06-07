from pathlib import Path

from toga_cocoa.libs import (
    NSBitmapImageFileType,
    NSBitmapImageRep,
    NSData,
    NSImage,
)


class Image:
    def __init__(self, interface, path=None, data=None):
        self.interface = interface

        if path:
            self.native = NSImage.alloc().initWithContentsOfFile(str(path))
        else:
            nsdata = NSData.dataWithBytes(data, length=len(data))
            self.native = NSImage.alloc().initWithData(nsdata)

    def get_width(self):
        return self.native.size.width

    def get_height(self):
        return self.native.size.height

    def save(self, path):
        path = Path(path)
        try:
            filetype = {
                ".jpg": NSBitmapImageFileType.JPEG,
                ".jpeg": NSBitmapImageFileType.JPEG,
                ".png": NSBitmapImageFileType.PNG,
                ".gif": NSBitmapImageFileType.GIF,
                ".bmp": NSBitmapImageFileType.BMP,
                ".tiff": NSBitmapImageFileType.TIFF,
            }[path.suffix.lower()]
            str_path = str(path)
        except KeyError:
            raise ValueError(f"Don't know how to save image of type {path.suffix!r}")

        bitmapData = NSBitmapImageRep.representationOfImageRepsInArray(
            self.native.representations,
            usingType=filetype,
            properties=None,
        )
        bitmapData.writeToFile(str_path, atomically=True)
