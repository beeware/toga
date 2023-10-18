from math import degrees, pi

import System.Windows.Forms as WinForms
from System.Drawing import (
    Bitmap,
    Graphics,
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
    PixelOffsetMode,
    SmoothingMode,
)
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream

from toga.widgets.canvas import Baseline, FillRule
from toga_winforms.colors import native_color

from ..libs.wrapper import WeakrefCallable
from .box import Box


class WinformContext:
    def __init__(self):
        super().__init__()
        self.graphics = None
        self.matrix = Matrix()
        self.clear_paths()

    def clear_paths(self):
        self.paths = []
        self.start_point = None
        self.at_start_point = False

    @property
    def current_path(self):
        if len(self.paths) == 0:
            self.add_path()
        return self.paths[-1]

    def add_path(self):
        self.paths.append(GraphicsPath())

    # Because the GraphicsPath API works in terms of segments rather than points, it has
    # nowhere to save the starting point of each figure before we use it. In all other
    # situations, we can get the last point from the GraphicsPath itself.
    #
    # default_x and default_y should be set as described in the HTML spec under "ensure
    # there is a subpath".
    def get_last_point(self, default_x, default_y):
        if self.at_start_point:
            self.at_start_point = False
            return self.start_point
        elif self.current_path.PointCount:
            return self.current_path.GetLastPoint()
        else:
            # Since we're returning start_point for immediate use, we don't set
            # at_start_point here.
            self.start_point = PointF(default_x, default_y)
            return self.start_point


class Canvas(Box):
    def create(self):
        super().create()
        self.native.DoubleBuffered = True
        self.native.Paint += WeakrefCallable(self.winforms_paint)
        self.native.Resize += WeakrefCallable(self.winforms_resize)
        self.native.MouseDown += WeakrefCallable(self.winforms_mouse_down)
        self.native.MouseMove += WeakrefCallable(self.winforms_mouse_move)
        self.native.MouseUp += WeakrefCallable(self.winforms_mouse_up)
        self.string_format = StringFormat.GenericTypographic
        self.dragging = False
        self.states = []

    # The control automatically paints the background color, so painting it again here
    # would give incorrect results if it was semi-transparent. But we do paint it in
    # get_image_data.
    def winforms_paint(self, panel, event, *args):
        context = WinformContext()
        self.reset_transform(context)
        context.graphics = event.Graphics
        context.graphics.PixelOffsetMode = PixelOffsetMode.HighQuality
        context.graphics.SmoothingMode = SmoothingMode.AntiAlias
        self.interface.context._draw(self, draw_context=context)

    def winforms_resize(self, *args):
        self.interface.on_resize(
            None,
            width=self.scale_out(self.native.Width),
            height=self.scale_out(self.native.Height),
        )

    def winforms_mouse_down(self, obj, mouse_event):
        x, y = map(self.scale_out, (mouse_event.X, mouse_event.Y))
        if mouse_event.Button == WinForms.MouseButtons.Left:
            if mouse_event.Clicks == 2:
                self.interface.on_activate(None, x, y)
            else:
                self.interface.on_press(None, x, y)
                self.dragging = True
        elif mouse_event.Button == WinForms.MouseButtons.Right:
            self.interface.on_alt_press(None, x, y)
            self.dragging = True
        else:  # pragma: no cover
            pass

    def winforms_mouse_move(self, obj, mouse_event):
        if not self.dragging:
            return
        x, y = map(self.scale_out, (mouse_event.X, mouse_event.Y))
        if mouse_event.Button == WinForms.MouseButtons.Left:
            self.interface.on_drag(None, x, y)
        elif mouse_event.Button == WinForms.MouseButtons.Right:
            self.interface.on_alt_drag(None, x, y)
        else:  # pragma: no cover
            pass

    def winforms_mouse_up(self, obj, mouse_event):
        self.dragging = False
        x, y = map(self.scale_out, (mouse_event.X, mouse_event.Y))
        if mouse_event.Button == WinForms.MouseButtons.Left:
            self.interface.on_release(None, x, y)
        elif mouse_event.Button == WinForms.MouseButtons.Right:
            self.interface.on_alt_release(None, x, y)
        else:  # pragma: no cover
            pass

    def redraw(self):
        self.native.Invalidate()

    # Context management

    def push_context(self, draw_context, **kwargs):
        self.states.append(draw_context.matrix)
        draw_context.matrix = draw_context.matrix.Clone()

    def pop_context(self, draw_context, **kwargs):
        draw_context.matrix = self.states.pop()

    # Basic paths

    def begin_path(self, draw_context, **kwargs):
        draw_context.clear_paths()

    # We don't use current_path.CloseFigure, because that causes the dash pattern to
    # start on the last segment of the path rather than the first one.
    def close_path(self, draw_context, **kwargs):
        start = draw_context.start_point
        if start:
            draw_context.current_path.AddLine(
                draw_context.get_last_point(start.X, start.Y), start
            )
            self.move_to(start.X, start.Y, draw_context)

    def move_to(self, x, y, draw_context, **kwargs):
        draw_context.current_path.StartFigure()
        draw_context.start_point = PointF(x, y)
        draw_context.at_start_point = True

    def line_to(self, x, y, draw_context, **kwargs):
        draw_context.current_path.AddLine(
            draw_context.get_last_point(x, y), PointF(x, y)
        )

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, draw_context, **kwargs):
        draw_context.current_path.AddBezier(
            draw_context.get_last_point(cp1x, cp1y),
            PointF(cp1x, cp1y),
            PointF(cp2x, cp2y),
            PointF(x, y),
        )

    # A Quadratic curve is a dimensionally reduced Bézier Cubic curve;
    # we can convert the single Quadratic control point into the
    # 2 control points required for the cubic Bézier.
    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, **kwargs):
        last_point = draw_context.get_last_point(cpx, cpy)
        x0, y0 = (last_point.X, last_point.Y)
        draw_context.current_path.AddBezier(
            last_point,
            PointF(
                x0 + 2 / 3 * (cpx - x0),
                y0 + 2 / 3 * (cpy - y0),
            ),
            PointF(
                x + 2 / 3 * (cpx - x),
                y + 2 / 3 * (cpy - y),
            ),
            PointF(x, y),
        )

    def arc(
        self, x, y, radius, startangle, endangle, anticlockwise, draw_context, **kwargs
    ):
        sweepangle = endangle - startangle
        if anticlockwise:
            if sweepangle > 0:
                sweepangle -= 2 * pi
        else:
            if sweepangle < 0:
                sweepangle += 2 * pi

        rect = RectangleF(x - radius, y - radius, 2 * radius, 2 * radius)
        draw_context.current_path.AddArc(rect, degrees(startangle), degrees(sweepangle))

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
        **kwargs,
    ):
        # Transformations apply not to individual points, but to entire GraphicsPath
        # objects, so we must create a separate one for this shape.
        draw_context.add_path()

        # The current transform will be applied when the path is filled or stroked, so
        # make sure we don't apply it now.
        self.push_context(draw_context)
        draw_context.matrix.Reset()

        self.translate(x, y, draw_context)
        self.rotate(rotation, draw_context)
        if radiusx >= radiusy:
            self.scale(1, radiusy / radiusx, draw_context)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise, draw_context)
        else:
            self.scale(radiusx / radiusy, 1, draw_context)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise, draw_context)

        draw_context.current_path.Transform(draw_context.matrix)

        # Set up a fresh GraphicsPath for the next operation.
        self.pop_context(draw_context)
        draw_context.add_path()

    def rect(self, x, y, width, height, draw_context, **kwargs):
        rect = RectangleF(x, y, width, height)
        draw_context.current_path.AddRectangle(rect)

    # Drawing Paths

    def fill(self, color, fill_rule, draw_context, **kwargs):
        brush = SolidBrush(native_color(color))
        for path in draw_context.paths:
            if fill_rule == FillRule.EVENODD:
                path.FillMode = FillMode.Alternate
            else:  # Default to NONZERO
                path.FillMode = FillMode.Winding
            path.Transform(draw_context.matrix)
            draw_context.graphics.FillPath(brush, path)
        draw_context.paths.clear()

    def stroke(self, color, line_width, line_dash, draw_context, **kwargs):
        pen = Pen(native_color(color), self.scale_in(line_width, rounding=None))
        if line_dash is not None:
            pen.DashPattern = [ld / line_width for ld in line_dash]

        for path in draw_context.paths:
            path.Transform(draw_context.matrix)
            draw_context.graphics.DrawPath(pen, path)
        draw_context.paths.clear()

    # Transformations

    def rotate(self, radians, draw_context, **kwargs):
        draw_context.matrix.Rotate(degrees(radians))

    def scale(self, sx, sy, draw_context, **kwargs):
        draw_context.matrix.Scale(sx, sy)

    def translate(self, tx, ty, draw_context, **kwargs):
        draw_context.matrix.Translate(tx, ty)

    def reset_transform(self, draw_context, **kwargs):
        draw_context.matrix.Reset()
        self.scale(self.dpi_scale, self.dpi_scale, draw_context)

    # Text
    def write_text(self, text, x, y, font, baseline, draw_context, **kwargs):
        for op in ["fill", "stroke"]:
            if color := kwargs.pop(f"{op}_color", None):
                self._text_path(text, x, y, font, baseline, draw_context)
                getattr(self, op)(color, draw_context=draw_context, **kwargs)

    def _text_path(self, text, x, y, font, baseline, draw_context):
        lines = text.splitlines()
        line_height = font.metric("LineSpacing")
        total_height = line_height * len(lines)

        if baseline == Baseline.TOP:
            top = y
        elif baseline == Baseline.MIDDLE:
            top = y - (total_height / 2)
        elif baseline == Baseline.BOTTOM:
            top = y - total_height
        else:
            # Default to Baseline.ALPHABETIC
            top = y - font.metric("CellAscent")

        for line_num, line in enumerate(lines):
            draw_context.current_path.AddString(
                line,
                font.native.FontFamily,
                font.native.Style.value__,
                font.metric("EmHeight"),
                PointF(x, top + (line_height * line_num)),
                self.string_format,
            )

    def measure_text(self, text, font):
        graphics = self.native.CreateGraphics()
        sizes = [
            graphics.MeasureString(line, font.native, 2**31 - 1, self.string_format)
            for line in text.splitlines()
        ]
        return (
            self.scale_out(max(size.Width for size in sizes)),
            font.metric("LineSpacing") * len(sizes),
        )

    def get_image_data(self):
        width, height = (self.native.Width, self.native.Height)
        bitmap = Bitmap(width, height)
        rect = Rectangle(0, 0, width, height)
        graphics = Graphics.FromImage(bitmap)
        graphics.Clear(self.native.BackColor)
        self.native.OnPaint(WinForms.PaintEventArgs(graphics, rect))

        stream = MemoryStream()
        bitmap.Save(stream, ImageFormat.Png)
        return stream.ToArray()
