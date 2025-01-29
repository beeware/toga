from io import BytesIO

from PIL import Image
from System.Windows.Forms import MouseButtons, Panel

from .base import SimpleProbe


class CanvasProbe(SimpleProbe):
    native_class = Panel

    def reference_variant(self, reference):
        if reference in {"multiline_text", "write_text"}:
            return f"{reference}-winforms"
        return reference

    def get_image(self):
        return Image.open(BytesIO(self.impl.get_image_data()))

    async def mouse_press(self, x, y, **kwargs):
        self.native.OnMouseDown(self.mouse_event(x, y, **kwargs))
        self.native.OnMouseUp(self.mouse_event(x, y, **kwargs))

    async def mouse_activate(self, x, y, **kwargs):
        self.native.OnMouseDown(self.mouse_event(x, y, **kwargs))
        self.native.OnMouseUp(self.mouse_event(x, y, **kwargs))
        self.native.OnMouseDown(self.mouse_event(x, y, clicks=2, **kwargs))
        self.native.OnMouseUp(self.mouse_event(x, y, clicks=2, **kwargs))

    async def mouse_drag(self, x1, y1, x2, y2, **kwargs):
        # Without a mouse button pressed, a move event should be ignored.
        move_event = self.mouse_event((x1 + x2) // 2, (y1 + y2) // 2, **kwargs)
        self.native.OnMouseMove(move_event)

        self.native.OnMouseDown(self.mouse_event(x1, y1, **kwargs))
        self.native.OnMouseMove(move_event)
        self.native.OnMouseUp(self.mouse_event(x2, y2, **kwargs))

    async def alt_mouse_press(self, x, y):
        await self.mouse_press(x, y, button=MouseButtons.Right)

    async def alt_mouse_drag(self, x1, y1, x2, y2):
        await self.mouse_drag(x1, y1, x2, y2, button=MouseButtons.Right)
