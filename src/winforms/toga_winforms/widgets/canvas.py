from travertino.colors import WHITE

from toga.widgets.canvas import Context
from .box import Box
from toga_winforms.colors import native_color
from toga_winforms.libs import Pen, Graphics


class WinformContext(Context):

    def __init__(self):
        super(WinformContext, self).__init__()
        self.graphics = None
        self.start_point = None
        self.last_point = None


class Canvas(Box):

    def create(self):
        super(Canvas, self).create()
        self.native.Paint += self.paint
        self.native.Resize += self.resize

    def set_on_resize(self, handler):
        pass

    def paint(self, panel, event, *args):
        context = WinformContext()
        context.graphics = event.Graphics
        context.graphics.Clear(native_color(WHITE))
        self.interface._draw(self, draw_context=context)

    def resize(self, *args):
        """Called on widget resize, and calls the handler set on the interface,
        if any.
        """
        if self.interface.on_resize:
            self.interface.on_resize(self.interface)


    def redraw(self):
        self.native.Invalidate()

    def stroke(self, color, line_width, line_dash, draw_context, *args, **kwargs):
        pass

    def closed_path(self, x, y, draw_context, *args, **kwargs):
        self.line_to(x, y, draw_context, *args, **kwargs)

    def move_to(self, x, y, draw_context, *args, **kwargs):
        draw_context.last_point = (x, y)

    def line_to(self, x, y, draw_context, *args, **kwargs):
        color = native_color(kwargs.get("stroke_color", None))
        pen = Pen(color)
        draw_context.graphics.DrawLine(pen, *draw_context.last_point, x, y)
        draw_context.last_point = (x, y)
