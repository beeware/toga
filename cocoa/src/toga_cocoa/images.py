from ctypes import POINTER, c_char, cast
from pathlib import Path

from toga_cocoa.libs import (
    NSBitmapImageFileType,
    NSBitmapImageRep,
    NSData,
    NSImage,
)


def nsdata_to_bytes(data: NSData) -> bytes:
    """Convert an NSData into a raw bytes representation"""
    # data is an NSData object that has .bytes as a c_void_p, and a .length. Cast to
    # POINTER(c_char) to get an addressable array of bytes, and slice that array to
    # the known length. We don't use c_char_p because it has handling of NUL
    # termination, and POINTER(c_char) allows array subscripting.
    return cast(data.bytes, POINTER(c_char))[: data.length]


class Image:
    RAW_TYPE = NSImage

    def __init__(self, interface, path=None, data=None, raw=None):
        self.interface = interface

        if path:
            self.native = NSImage.alloc().initWithContentsOfFile(str(path))
            if self.native is None:
                raise ValueError(f"Unable to load image from {path}")
        elif data:
            nsdata = NSData.dataWithBytes(data, length=len(data))
            self.native = NSImage.alloc().initWithData(nsdata)
            if self.native is None:
                raise ValueError("Unable to load image from data")
        else:
            self.native = raw

    def get_width(self):
        return self.native.size.width

    def get_height(self):
        return self.native.size.height

    def get_data(self):
        # A file created from a data source won't necessarily have a pre-existing PNG
        # representation. Create a TIFF representation, then convert to PNG.
        bitmap_rep = NSBitmapImageRep.imageRepWithData(self.native.TIFFRepresentation)
        image_data = bitmap_rep.representationUsingType(
            NSBitmapImageFileType.PNG,
            properties=None,
        )
        return nsdata_to_bytes(image_data)

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
