import math

import System.Windows.Forms as WinForms
from System.Drawing import (
    Bitmap,
    Drawing2D,
    Pen,
    PointF,
    Rectangle,
    RectangleF,
    SolidBrush,
    StringFormat,
)
from System.Drawing.Drawing2D import (
    FillMode,
    GraphicsPath,
    Matrix,
)
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream
from travertino.colors import WHITE

from toga.widgets.canvas import FillRule
from toga_winforms.colors import native_color

from .box import Box


class WinformContext:
    def __init__(self):
        super().__init__()
        self.graphics = None
        self.paths = []
        self.start_point = None
        self.last_point = None
        self.matrix = None

    @property
    def current_path(self):
        if len(self.paths) == 0:
            self.add_path()
        return self.paths[-1]

    def add_path(self):
        self.paths.append(GraphicsPath())

    @property
    def matrix(self):
        if self._matrix is None:
            self._matrix = Matrix()
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = matrix


class Canvas(Box):
    def create(self):
        super().create()
        self.native.DoubleBuffered = True
        self.native.Paint += self.winforms_paint
        self.native.Resize += self.winforms_resize
        self.native.MouseDown += self.winforms_mouse_down
        self.native.MouseMove += self.winforms_mouse_move
        self.native.MouseUp += self.winforms_mouse_up
        self.dragging = False
        self.states = []

    def winforms_paint(self, panel, event, *args):
        context = WinformContext()
        context.graphics = event.Graphics
        context.graphics.Clear(native_color(WHITE))
        context.graphics.SmoothingMode = Drawing2D.SmoothingMode.AntiAlias
        self.interface.context._draw(self, draw_context=context)

    def winforms_resize(self, *args):
        self.interface.on_resize(
            None,
            width=self.scale_out(self.native.Width),
            height=self.scale_out(self.native.Height),
        )

    def winforms_mouse_down(self, obj, mouse_event):
        if mouse_event.Button == WinForms.MouseButtons.Left:
            if mouse_event.Clicks == 2:
                self.interface.on_activate(None, mouse_event.X, mouse_event.Y)
            else:
                self.interface.on_press(None, mouse_event.X, mouse_event.Y)
                self.dragging = True
        elif mouse_event.Button == WinForms.MouseButtons.Right:
            self.interface.on_alt_press(None, mouse_event.X, mouse_event.Y)
            self.dragging = True

    def winforms_mouse_move(self, obj, mouse_event):
        if not self.dragging:
            return
        if mouse_event.Button == WinForms.MouseButtons.Left:
            self.interface.on_drag(None, mouse_event.X, mouse_event.Y)
        elif mouse_event.Button == WinForms.MouseButtons.Right:
            self.interface.on_alt_drag(None, mouse_event.X, mouse_event.Y)

    def winforms_mouse_up(self, obj, mouse_event):
        if mouse_event.Button == WinForms.MouseButtons.Left:
            self.interface.on_release(None, mouse_event.X, mouse_event.Y)
        elif mouse_event.Button == WinForms.MouseButtons.Right:
            self.interface.on_alt_release(None, mouse_event.X, mouse_event.Y)
        self.dragging = False

    def redraw(self):
        self.native.Invalidate()

    def create_pen(self, color=None, line_width=None, line_dash=None):
        pen = Pen(native_color(color))
        if line_width is not None:
            pen.Width = line_width
        if line_dash is not None:
            pen.DashPattern = tuple(map(float, line_dash))
        return pen

    def create_brush(self, color):
        return SolidBrush(native_color(color))

    # Context management

    def push_context(self, draw_context, **kwargs):
        self.states.append(draw_context.graphics.Save())

    def pop_context(self, draw_context, **kwargs):
        draw_context.graphics.Restore(self.states.pop())

    # Basic paths

    def begin_path(self, draw_context, **kwargs):
        draw_context.add_path()

    def close_path(self, draw_context, **kwargs):
        draw_context.current_path.CloseFigure()
        draw_context.last_point = draw_context.start_point

    def move_to(self, x, y, draw_context, **kwargs):
        draw_context.add_path()
        draw_context.start_point = draw_context.last_point = (x, y)

    def line_to(self, x, y, draw_context, **kwargs):
        draw_context.current_path.AddLine(
            draw_context.last_point[0], draw_context.last_point[1], x, y
        )
        draw_context.last_point = (x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, draw_context, **kwargs):
        draw_context.current_path.AddBezier(
            PointF(draw_context.last_point[0], draw_context.last_point[1]),
            PointF(cp1x, cp1y),
            PointF(cp2x, cp2y),
            PointF(x, y),
        )
        draw_context.last_point = (x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, **kwargs):
        draw_context.current_path.AddCurve(
            [
                PointF(draw_context.last_point[0], draw_context.last_point[1]),
                PointF(cpx, cpy),
                PointF(x, y),
            ]
        )
        draw_context.last_point = (x, y)

    def arc(
        self, x, y, radius, startangle, endangle, anticlockwise, draw_context, **kwargs
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
        **kwargs
    ):
        rect = RectangleF(x - radiusx, y - radiusy, 2 * radiusx, 2 * radiusy)
        draw_context.current_path.AddArc(
            rect, math.degrees(startangle), math.degrees(endangle - startangle)
        )
        draw_context.last_point = (
            x + radiusx * math.cos(endangle),
            y + radiusy * math.sin(endangle),
        )

    def rect(self, x, y, width, height, draw_context, **kwargs):
        rect = RectangleF(x, y, width, height)
        draw_context.current_path.AddRectangle(rect)

    # Drawing Paths

    def fill(self, color, fill_rule, draw_context, **kwargs):
        brush = self.create_brush(color)
        fill_mode = self.native_fill_rule(fill_rule)
        for path in draw_context.paths:
            if fill_mode is not None:
                path.FillMode = fill_mode
            if draw_context.matrix is not None:
                path.Transform(draw_context.matrix)
            draw_context.graphics.FillPath(brush, path)
        draw_context.paths.clear()

    def native_fill_rule(self, fill_rule):
        if fill_rule == FillRule.EVENODD:
            return FillMode.Alternate
        if fill_rule == FillRule.NONZERO:
            return FillMode.Winding
        return None

    def stroke(self, color, line_width, line_dash, draw_context, **kwargs):
        pen = self.create_pen(color=color, line_width=line_width, line_dash=line_dash)
        for path in draw_context.paths:
            if draw_context.matrix is not None:
                path.Transform(draw_context.matrix)
            draw_context.graphics.DrawPath(pen, path)
        draw_context.paths.clear()

    # Transformations

    def rotate(self, radians, draw_context, **kwargs):
        draw_context.matrix.Rotate(math.degrees(radians))

    def scale(self, sx, sy, draw_context, **kwargs):
        draw_context.matrix.Scale(sx, sy)

    def translate(self, tx, ty, draw_context, **kwargs):
        draw_context.matrix.Translate(tx, ty)

    def reset_transform(self, draw_context, **kwargs):
        draw_context.matrix = None

    # Text
    def write_text(self, text, x, y, font, draw_context, **kwargs):
        full_height = 0
        em_height = font.native.Size * self.native.CreateGraphics().DpiY / 72
        font_family = font.native.FontFamily
        font_style = font.native.Style.value__
        for line in text.splitlines():
            # height includes some padding, so it will be slightly more than em_height.
            _, height = self.measure_text(line, font)
            origin = PointF(x, y + full_height - height)
            draw_context.current_path.AddString(
                line, font_family, font_style, em_height, origin, StringFormat()
            )
            full_height += height

    def measure_text(self, text, font):
        sizes = [
            WinForms.TextRenderer.MeasureText(line, font.native)
            for line in text.splitlines()
        ]
        width = max([size.Width for size in sizes])
        height = sum([size.Height for size in sizes])
        return (width, height)

    def get_image_data(self):
        width, height = (
            self.interface.layout.content_width,
            self.interface.layout.content_height,
        )
        bitmap = Bitmap(width, height)
        rect = Rectangle(0, 0, width, height)
        self.native.DrawToBitmap(bitmap, rect)
        stream = MemoryStream()
        bitmap.Save(stream, ImageFormat.Png)
        return stream.ToArray()
