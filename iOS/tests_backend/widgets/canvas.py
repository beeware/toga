from io import BytesIO

import pytest
from PIL import Image
from rubicon.objc import NSPoint, ObjCClass

from toga_iOS.libs import UIView

from .base import SimpleProbe
from .utils import MockTouch

# Touch events generate a Set of 1 event.
NSSet = ObjCClass("NSSet")


class CanvasProbe(SimpleProbe):
    native_class = UIView

    def reference_variant(self, reference):
        # System fonts and sizes are platform specific
        if reference in {
            "multiline_text",
            "write_text",
            "write_text_and_path",
            "deprecated_tutorial",
        }:
            return f"{reference}-iOS"
        else:
            return reference

    def get_image(self):
        return Image.open(BytesIO(self.impl.get_image_data()))

    async def mouse_press(self, x, y):
        touch = MockTouch.alloc().init()
        touches = NSSet.setWithObject(touch)

        touch.position = NSPoint(x, y)
        self.native.touchesBegan(touches, withEvent=None)
        self.native.touchesEnded(touches, withEvent=None)

    async def mouse_activate(self, x, y):
        pytest.skip("Activation not supported on iOS")

    async def mouse_drag(self, x1, y1, x2, y2):
        touch = MockTouch.alloc().init()
        touches = NSSet.setWithObject(touch)

        touch.position = NSPoint(x1, y1)
        self.native.touchesBegan(touches, withEvent=None)

        touch.position = NSPoint((x1 + x2) // 2, (y1 + y2) // 2)
        self.native.touchesMoved(touches, withEvent=None)

        touch.position = NSPoint(x2, y2)
        self.native.touchesEnded(touches, withEvent=None)

    async def alt_mouse_press(self, x, y):
        pytest.skip("Alternate handling not supported on iOS")

    async def alt_mouse_drag(self, x1, y1, x2, y2):
        pytest.skip("Alternate handling not supported on iOS")
