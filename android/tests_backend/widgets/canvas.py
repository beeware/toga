from io import BytesIO

import pytest
from android.os import SystemClock
from android.view import MotionEvent
from org.beeware.android import DrawHandlerView
from PIL import Image

from .base import SimpleProbe


class CanvasProbe(SimpleProbe):
    native_class = DrawHandlerView

    def reference_variant(self, reference):
        if reference in {"multiline_text", "write_text"}:
            return f"{reference}-android"
        return reference

    def get_image(self):
        return Image.open(BytesIO(self.impl.get_image_data()))

    def motion_event(self, action, x, y):
        time = SystemClock.uptimeMillis()
        super().motion_event(
            time, time, action, x * self.scale_factor, y * self.scale_factor
        )

    async def mouse_press(self, x, y):
        self.motion_event(MotionEvent.ACTION_DOWN, x, y)
        self.motion_event(MotionEvent.ACTION_UP, x, y)

    async def mouse_activate(self, x, y):
        pytest.skip("Activation not supported on this platform")

    async def mouse_drag(self, x1, y1, x2, y2):
        self.motion_event(MotionEvent.ACTION_DOWN, x1, y1)
        self.motion_event(MotionEvent.ACTION_MOVE, (x1 + x2) / 2, (y1 + y2) / 2)
        self.motion_event(MotionEvent.ACTION_UP, x2, y2)

    async def alt_mouse_press(self, x, y):
        pytest.skip("Alternate handling not supported on this platform")

    async def alt_mouse_drag(self, x1, y1, x2, y2):
        pytest.skip("Alternate handling not supported on this platform")
