from io import BytesIO

from PIL import Image, ImageCms
from rubicon.objc import NSPoint

from toga.colors import TRANSPARENT
from toga.images import Image as TogaImage
from toga_cocoa.libs import NSEventType, NSView

from .base import SimpleProbe
from .properties import toga_color


class CanvasProbe(SimpleProbe):
    native_class = NSView

    @property
    def background_color(self):
        if self.native.backgroundColor:
            return toga_color(self.native.backgroundColor)
        else:
            return TRANSPARENT

    def reference_variant(self, reference):
        if reference in {"multiline_text", "write_text"}:
            # System font and default size is platform dependent.
            return f"{reference}-macOS"
        return reference

    def get_image(self):
        image = Image.open(BytesIO(TogaImage(self.impl.get_image_data()).data))

        try:
            # If the image has an ICC profile, convert it into sRGB colorspace.
            # This is needed when attached to an laptop display; otherwise the RGB
            # values in colors in the image won't *quite* match.
            icc = image.info["icc_profile"]
            src_profile = ImageCms.ImageCmsProfile(BytesIO(icc))
            dst_profile = ImageCms.createProfile("sRGB")
            return ImageCms.profileToProfile(image, src_profile, dst_profile)
        except KeyError:
            return image

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
