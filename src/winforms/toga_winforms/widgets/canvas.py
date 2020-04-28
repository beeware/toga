import math

from travertino.colors import WHITE

from toga.widgets.canvas import Context
from .box import Box
from toga_winforms.colors import native_color
from toga_winforms.libs import Pen, SolidBrush, GraphicsPath, Rectangle, PointF


class WinformContext(Context):

    def __init__(self):
        super(WinformContext, self).__init__()
        self.graphics = None
        self.path = None
        self.start_point = None
        self.last_point = None


class Canvas(Box):

    def create(self):
        super(Canvas, self).create()
        self.native.Paint += self.winforms_paint
        self.native.Resize += self.winforms_resize

    def set_on_resize(self, handler):
        pass

    def winforms_paint(self, panel, event, *args):
        context = WinformContext()
        context.graphics = event.Graphics
        context.graphics.Clear(native_color(WHITE))
        self.interface._draw(self, draw_context=context)

    def winforms_resize(self, *args):
        """Called on widget resize, and calls the handler set on the interface,
        if any.
        """
        if self.interface.on_resize:
            self.interface.on_resize(self.interface)

    def redraw(self):
        self.native.Invalidate()

    def create_pen(self, kwargs):
        color = native_color(kwargs.get("stroke_color", None))
        pen = Pen(color)
        return pen

    # Basic paths

    def new_path(self, draw_context, *args, **kwargs):
        draw_context.path = GraphicsPath()

    def closed_path(self, x, y, draw_context, *args, **kwargs):
        self.line_to(x, y, draw_context, *args, **kwargs)

    def move_to(self, x, y, draw_context, *args, **kwargs):
        draw_context.last_point = (x, y)

    def line_to(self, x, y, draw_context, *args, **kwargs):
        if draw_context.path is not None:
            draw_context.path.AddLine(*draw_context.last_point, x, y)
        else:
            pen = self.create_pen(kwargs)
            draw_context.graphics.DrawLine(pen, *draw_context.last_point, x, y)
        draw_context.last_point = (x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, draw_context, *args, **kwargs):
        point1, point2, point3, point4 = (
            PointF(*draw_context.last_point),
            PointF(cp1x, cp1y),
            PointF(cp2x, cp2y),
            PointF(x, y)
        )
        if draw_context.path is not None:
            draw_context.path.AddBezier(point1, point2, point3, point4)
        else:
            pen = self.create_pen(kwargs)
            draw_context.graphics.DrawBezier(pen, point1, point2, point3, point4)
        draw_context.last_point = (x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, *args, **kwargs):
        point1, point2, point3 = PointF(*draw_context.last_point), PointF(cpx, cpy), PointF(x, y)
        if draw_context.path is not None:
            draw_context.path.AddCurve([point1, point2, point3])
        else:
            pen = self.create_pen(kwargs)
            draw_context.graphics.DrawCurve(pen, [point1, point2, point3])
        draw_context.last_point = (x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, draw_context, *args, **kwargs):
        x_min, y_min = x - radius, y - radius
        if draw_context.path is not None:
            draw_context.path.AddArc(
                x_min, y_min, 2 * radius, 2 * radius, math.degrees(startangle), math.degrees(endangle - startangle)
            )
        else:
            pen = self.create_pen(kwargs)
            draw_context.graphics.DrawArc(
                pen, x_min, y_min, 2 * radius, 2 * radius, math.degrees(startangle), math.degrees(endangle - startangle)
            )
        draw_context.last_point = (
            x + radius * math.cos(endangle),
            y + radius * math.sin(endangle)
        )

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise,
                draw_context, *args, **kwargs):
        if draw_context.path is not None:
            draw_context.path.AddEllipse(
                x - radiusx, y - radiusy, 2 * radiusx, 2 * radiusy
            )
        else:
            pen = self.create_pen(kwargs)
            draw_context.graphics.DrawEllipse(
                pen, x - radiusx, y - radiusy, 2 * radiusx, 2 * radiusy
            )

    def rect(self, x, y, width, height, draw_context, *args, **kwargs):
        rect = Rectangle(int(x), int(y), int(width), int(height))
        if draw_context.path is not None:
            draw_context.path.AddRectangle(rect)
        else:
            pen = self.create_pen(kwargs)
            draw_context.graphics.DrawRectangle(pen, rect)

    # Drawing Paths

    def apply_color(self, color, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.apply_color()')

    def fill(self, color, fill_rule, preserve, draw_context, *args, **kwargs):
        brush = SolidBrush(native_color(color))
        draw_context.graphics.FillPath(brush, draw_context.path)

    def stroke(self, color, line_width, line_dash, draw_context, *args, **kwargs):
        pass

    # Transformations

    def rotate(self, radians, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.rotate()')

    def scale(self, sx, sy, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.scale()')

    def translate(self, tx, ty, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.translate()')

    def reset_transform(self, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.reset_transform()')

    # Text

    def write_text(self, text, x, y, font, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.write_text()')

    def measure_text(self, text, font, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.measure_text()')
