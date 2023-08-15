from toga.screen import Screen as ScreenInterface
from toga_cocoa.libs import (
    CGDisplayCreateImage,
    CGMainDisplayID,
    NSBitmapImageFileType,
    NSBitmapImageRep,
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
        return self.native.localizedName

    def get_origin(self):
        frame_native = self.native.frame
        return (frame_native.origin.x, frame_native.origin.y)

    def get_size(self):
        frame_native = self.native.frame
        return (frame_native.size.width, frame_native.size.height)

    def get_image_data(self):
        screenshot_frame = self.native.frame()
        cg_image = CGDisplayCreateImage(CGMainDisplayID(), screenshot_frame)
        bitmap_rep = NSBitmapImageRep.alloc().initWithCGImage(cg_image)
        data = bitmap_rep.representationUsingType(
            NSBitmapImageFileType.PNG,
            properties=None,
        )
        return data
