from io import BytesIO

from PIL import Image
from System.Drawing import Color
from System.Windows.Forms import MouseButtons, Panel

from .base import SimpleProbe
from .properties import toga_color


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

    @property
    def background_color(self):
        if self.native.BackColor == Color.Transparent:
            # When BackColor is set to Color.Transparent then send Color.Transparent as the parent
            # for asserting background color. This is because unlike other widgets, setting the
            # canvas widget's background to TRANSPARENT sets the BackColor to Color.Transparent,
            # instead of setting the canvas widget's BackColor the same as the parent's BackColor.
            #
            # See toga_winforms/widgets/canvas.py::set_background_color for why this is done so.
            return (toga_color(self.native.BackColor), toga_color(Color.Transparent), 1)
        else:
            return super().background_color
