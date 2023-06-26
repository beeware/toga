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

        try:
            # We *should* be able to do a direct NSImage.alloc.init...(),
            # but for some reason, this segfaults in some environments
            # when loading invalid images. On iOS we can avoid this by
            # using the class-level constructors; on macOS we need to
            # ensure we have a valid allocated image, then try to init it.
            image = NSImage.alloc().retain()
            if path:
                self.native = image.initWithContentsOfFile(str(path))
                if self.native is None:
                    raise ValueError(f"Unable to load image from {path}")
            else:
                nsdata = NSData.dataWithBytes(data, length=len(data))
                self.native = image.initWithData(nsdata)
                if self.native is None:
                    raise ValueError("Unable to load image from data")
        finally:
            image.release()

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
