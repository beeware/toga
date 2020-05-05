import math

from travertino.colors import WHITE

from toga.widgets.canvas import Context, FillRule
from .box import Box
from toga_winforms.colors import native_color
from toga_winforms.libs import (
    FillMode,
    Pen,
    SolidBrush,
    GraphicsPath,
    RectangleF,
    PointF,
    StringFormat,
    win_font_family
)
from ..libs.fonts import win_font_style


class WinformContext(Context):

    def __init__(self):
        super(WinformContext, self).__init__()
        self.graphics = None
        self.paths = []
        self.start_point = None
        self.last_point = None

    @property
    def current_path(self):
        if len(self.paths) == 0:
            self.add_path()
        return self.paths[-1]

    def add_path(self):
        self.paths.append(GraphicsPath())


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

    def create_pen(self, color=None, line_width=None, line_dash=None):
        pen = Pen(native_color(color))
        if line_width is not None:
            pen.Width = line_width
        if line_dash is not None:
            pen.DashPattern = line_dash
        return pen

    def create_brush(self, color):
        return SolidBrush(native_color(color))

    # Basic paths

    def new_path(self, draw_context, *args, **kwargs):
        draw_context.add_path()

    def closed_path(self, x, y, draw_context, *args, **kwargs):
        self.line_to(x, y, draw_context, *args, **kwargs)

    def move_to(self, x, y, draw_context, *args, **kwargs):
        draw_context.add_path()
        draw_context.last_point = (x, y)

    def line_to(self, x, y, draw_context, *args, **kwargs):
        ox, oy = int(draw_context.last_point[0]), int(draw_context.last_point[1])
        x, y = int(x), int(y)
        draw_context.current_path.AddLine(ox, oy, x, y)
        draw_context.last_point = (x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, draw_context, *args, **kwargs):
        point1, point2, point3, point4 = (
            PointF(*draw_context.last_point),
            PointF(cp1x, cp1y),
            PointF(cp2x, cp2y),
            PointF(x, y)
        )
        draw_context.current_path.AddBezier(point1, point2, point3, point4)
        draw_context.last_point = (x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, *args, **kwargs):
        point1, point2, point3 = PointF(*draw_context.last_point), PointF(cpx, cpy), PointF(x, y)
        draw_context.current_path.AddCurve([point1, point2, point3])
        draw_context.last_point = (x, y)

    def arc(
            self,
            x,
            y,
            radius,
            startangle,
            endangle,
            anticlockwise,
            draw_context,
            *args,
            **kwargs
    ):
        self.ellipse(
            x,
            y,
            radius,
            radius,
            0,
            startangle,
            endangle,
            anticlockwise,
            draw_context,
            *args,
            **kwargs
        )

    def ellipse(
            self,
            x,
            y,
            radiusx,
            radiusy,
            rotation,
            startangle,
            endangle,
            anticlockwise,
            draw_context,
            *args,
            **kwargs):
        rect = RectangleF(float(x - radiusx), float(y - radiusy), float(2 * radiusx), float(2 * radiusy))
        draw_context.current_path.AddArc(
            rect,
            math.degrees(startangle),
            math.degrees(endangle - startangle)
        )
        draw_context.last_point = (
            x + radiusx * math.cos(endangle),
            y + radiusy * math.sin(endangle)
        )

    def rect(self, x, y, width, height, draw_context, *args, **kwargs):
        rect = RectangleF(float(x), float(y), float(width), float(height))
        draw_context.current_path.AddRectangle(rect)

    # Drawing Paths

    def apply_color(self, color, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.apply_color()')

    def fill(self, color, fill_rule, preserve, draw_context, *args, **kwargs):
        brush = self.create_brush(color)
        fill_mode = self.native_fill_rule(fill_rule)
        for path in draw_context.paths:
            if fill_mode is not None:
                path.FillMode = fill_mode
            draw_context.graphics.FillPath(brush, path)
        draw_context.paths.clear()

    def native_fill_rule(self, fill_rule):
        if fill_rule == FillRule.EVENODD:
            return FillMode.Alternate
        if fill_rule == FillRule.NONZERO:
            return FillMode.Winding
        return None

    def stroke(self, color, line_width, line_dash, draw_context, *args, **kwargs):
        pen = self.create_pen(color=color, line_width=line_width, line_dash=line_dash)
        for path in draw_context.paths:
            draw_context.graphics.DrawPath(pen, path)
        draw_context.paths.clear()

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
        width, height = font.measure(text)
        origin = PointF(x, y - height)
        font_family = win_font_family(font.family)
        font_style = win_font_style(font.weight, font.style, font_family)
        draw_context.current_path.AddString(
            text, font_family, font_style, float(height), origin, StringFormat()
        )

    def measure_text(self, text, font, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.measure_text()')
