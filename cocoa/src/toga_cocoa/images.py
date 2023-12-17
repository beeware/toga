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

        try:
            # We *should* be able to do a direct NSImage.alloc.init...(), but if the
            # image file is invalid, the init fails, and returns NULL - but we've
            # created an ObjC instance, so when the object passes out of scope, Rubicon
            # tries to free it, which segfaults. To avoid this, we retain result of the
            # alloc() (overriding the default Rubicon behavior of alloc), then release
            # that reference once we're done. If the image was created successfully, we
            # temporarily have a reference count that is 1 higher than it needs to be;
            # if it fails, we don't end up with a stray release.
            image = NSImage.alloc().retain()
            if path:
                self.native = image.initWithContentsOfFile(str(path))
                if self.native is None:
                    raise ValueError(f"Unable to load image from {path}")
            elif data:
                nsdata = NSData.dataWithBytes(data, length=len(data))
                self.native = image.initWithData(nsdata)
                if self.native is None:
                    raise ValueError("Unable to load image from data")
            else:
                self.native = raw
        finally:
            image.release()

    def get_width(self):
        return self.native.size.width

    def get_height(self):
        return self.native.size.height

    def get_data(self):
        return nsdata_to_bytes(
            NSBitmapImageRep.representationOfImageRepsInArray(
                self.native.representations,
                usingType=NSBitmapImageFileType.PNG,
                properties=None,
            )
        )

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
