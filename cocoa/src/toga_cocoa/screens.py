from rubicon.objc import CGSize

from toga.screens import Screen as ScreenInterface
from toga.types import Position, Size
from toga_cocoa.libs import (
    NSImage,
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

    def get_origin(self) -> Position:
        frame_native = self.native.frame
        return Position(int(frame_native.origin.x), int(frame_native.origin.y))

    def get_size(self) -> Size:
        frame_native = self.native.frame
        return Size(int(frame_native.size.width), int(frame_native.size.height))

    def get_image_data(self):
        # Retrieve the device description dictionary for the NSScreen
        device_description = self.native.deviceDescription
        # Extract the CGDirectDisplayID from the device description
        cg_direct_display_id = device_description.objectForKey_(
            "NSScreenNumber"
        ).unsignedIntValue

        cg_image = core_graphics.CGDisplayCreateImage(
            cg_direct_display_id,
            self.native.frame,
        )
        # Get the size of the CGImage
        target_size = CGSize(
            core_graphics.CGImageGetWidth(cg_image),
            core_graphics.CGImageGetHeight(cg_image),
        )
        # Create an NSImage from the CGImage
        ns_image = NSImage.alloc().initWithCGImage(cg_image, size=target_size)
        return ns_image
