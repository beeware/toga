from pathlib import Path

from toga_cocoa.libs import (
    NSURL,
    NSBitmapImageFileType,
    NSBitmapImageRep,
    NSData,
    NSImage,
)


class Image:
    def __init__(self, interface, path=None, url=None, data=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = NSImage.alloc().initWithContentsOfFile(str(path))
        elif url:
            self.native = NSImage.alloc().initByReferencingURL(
                NSURL.URLWithString_(url)
            )
        elif data:
            if isinstance(data, NSData):
                nsdata = data
            else:
                nsdata = NSData.dataWithBytes(data, length=len(data))

            self.native = NSImage.alloc().initWithData(nsdata)

    def save(self, path):
        path = Path(path)
        try:
            if path.suffix == "":
                # If no suffix is provided in the filename, default to PNG,
                # and append that suffix to the filename.
                str_path = str(path) + ".png"
                filetype = NSBitmapImageFileType.PNG
            else:
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
            raise ValueError(f"Don't know how to save image of type {path.suffix}")

        bitmapData = NSBitmapImageRep.representationOfImageRepsInArray(
            self.native.representations,
            usingType=filetype,
            properties=None,
        )
        bitmapData.writeToFile(str_path, atomically=True)
