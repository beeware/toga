from io import BytesIO

from PIL import Image, ImageCms
from rubicon.objc import NSPoint

from toga_cocoa.libs import NSEventType, NSScreen, NSView

from .base import SimpleProbe


class CanvasProbe(SimpleProbe):
    native_class = NSView

    def scale(self):
        # Cocoa's backing store might not be at display coordinates.
        return int(NSScreen.mainScreen.backingScaleFactor)

    def get_image(self):
        image = Image.open(BytesIO(self.impl.get_image_data()))

        # Convert image data into sRGB colorspace.
        icc = image.info.get("icc_profile", "")
        src_profile = ImageCms.ImageCmsProfile(BytesIO(icc))
        dst_profile = ImageCms.createProfile("sRGB")
        image_srgb = ImageCms.profileToProfile(image, src_profile, dst_profile)

        return image_srgb

    def assert_image_size(self, image, width, height):
        # Cocoa reports image sizing in the natural screen coordinates, not the size of
        # the backing store.
        assert image.width == width
        assert image.height == height

    async def mouse_press(self, x, y):
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            self.native.convertPoint(NSPoint(x, y), toView=None),
        )

        await self.mouse_event(
            NSEventType.LeftMouseUp,
            self.native.convertPoint(NSPoint(x, y), toView=None),
        )

    async def mouse_activate(self, x, y):
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            self.native.convertPoint(NSPoint(x, y), toView=None),
        )

        await self.mouse_event(
            NSEventType.LeftMouseUp,
            self.native.convertPoint(NSPoint(x, y), toView=None),
        )

        await self.mouse_event(
            NSEventType.LeftMouseDown,
            self.native.convertPoint(NSPoint(x, y), toView=None),
            clickCount=2,
        )

        await self.mouse_event(
            NSEventType.LeftMouseUp,
            self.native.convertPoint(NSPoint(x, y), toView=None),
            clickCount=2,
        )

    async def mouse_drag(self, x1, y1, x2, y2):
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            self.native.convertPoint(NSPoint(x1, y1), toView=None),
        )

        await self.mouse_event(
            NSEventType.LeftMouseDragged,
            self.native.convertPoint(
                NSPoint((x1 + x2) // 2, (y1 + y2) // 2), toView=None
            ),
        )

        await self.mouse_event(
            NSEventType.LeftMouseUp,
            self.native.convertPoint(NSPoint(x2, y2), toView=None),
        )

    async def alt_mouse_press(self, x, y):
        await self.mouse_event(
            NSEventType.RightMouseDown,
            self.native.convertPoint(NSPoint(x, y), toView=None),
        )

        await self.mouse_event(
            NSEventType.RightMouseUp,
            self.native.convertPoint(NSPoint(x, y), toView=None),
        )

    async def alt_mouse_drag(self, x1, y1, x2, y2):
        await self.mouse_event(
            NSEventType.RightMouseDown,
            self.native.convertPoint(NSPoint(x1, y1), toView=None),
        )

        await self.mouse_event(
            NSEventType.RightMouseDragged,
            self.native.convertPoint(
                NSPoint((x1 + x2) // 2, (y1 + y2) // 2), toView=None
            ),
        )

        await self.mouse_event(
            NSEventType.RightMouseUp,
            self.native.convertPoint(NSPoint(x2, y2), toView=None),
        )
