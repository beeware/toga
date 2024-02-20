from ctypes import POINTER, c_char, cast
from pathlib import Path

from toga_iOS.libs import (
    NSData,
    UIImage,
    uikit,
)


def nsdata_to_bytes(data: NSData) -> bytes:
    """Convert an NSData into a raw bytes representation"""
    # data is an NSData object that has .bytes as a c_void_p, and a .length. Cast to
    # POINTER(c_char) to get an addressable array of bytes, and slice that array to
    # the known length. We don't use c_char_p because it has handling of NUL
    # termination, and POINTER(c_char) allows array subscripting.
    return cast(data.bytes, POINTER(c_char))[: data.length]


class Image:
    RAW_TYPE = UIImage

    def __init__(self, interface, path=None, data=None, raw=None):
        self.interface = interface

        if path:
            self.native = UIImage.imageWithContentsOfFile(str(path))
            if self.native is None:
                raise ValueError(f"Unable to load image from {path}")
        elif data:
            self.native = UIImage.imageWithData(
                NSData.dataWithBytes(data, length=len(data))
            )
            if self.native is None:
                raise ValueError("Unable to load image from data")
        else:
            self.native = raw

        self.native.retain()

    def __del__(self):
        if self.native:
            self.native.release()

    def get_width(self):
        return self.native.size.width

    def get_height(self):
        return self.native.size.height

    def get_data(self):
        return nsdata_to_bytes(NSData(uikit.UIImagePNGRepresentation(self.native)))

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
