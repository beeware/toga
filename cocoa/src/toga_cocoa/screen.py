from ctypes import POINTER, c_char, cast

from toga.screen import Screen as ScreenInterface
from toga_cocoa.libs import (
    NSBitmapImageFileType,
    NSBitmapImageRep,
    core_graphics,
)


class Screen:
    _instances = {}

    def __new__(cls, native):
        if native in cls._instances:
            return cls._instances[native]
        else:
            instance = super().__new__(cls)
            instance.interface = ScreenInterface(_impl=instance)
            instance.native = native
            cls._instances[native] = instance
            return instance

    def get_name(self):
        return str(self.native.localizedName)

    def get_origin(self):
        frame_native = self.native.frame
        return (int(frame_native.origin.x), int(frame_native.origin.y))

    def get_size(self):
        frame_native = self.native.frame
        return (int(frame_native.size.width), int(frame_native.size.height))

    def get_image_data(self):
        image = core_graphics.CGDisplayCreateImage(
            core_graphics.CGMainDisplayID(),
            self.native.frame,
        )
        bitmap_rep = NSBitmapImageRep.alloc().initWithCGImage(image)
        data = bitmap_rep.representationUsingType(
            NSBitmapImageFileType.PNG,
            properties=None,
        )

        # data is an NSData object that has .bytes as a c_void_p, and a .length. Cast to
        # POINTER(c_char) to get an addressable array of bytes, and slice that array to
        # the known length. We don't use c_char_p because it has handling of NUL
        # termination, and POINTER(c_char) allows array subscripting.
        return cast(data.bytes, POINTER(c_char))[: data.length]
