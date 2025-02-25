from math import degrees

import System.Windows.Forms as WinForms
from System import Array
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

from toga.colors import TRANSPARENT
from toga.constants import Baseline, FillRule
from toga.widgets.canvas import arc_to_bezier, sweepangle
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
        self.add_path()

    @property
    def current_path(self):
        return self.paths[-1]

    def add_path(self, start_point=None):
        self.paths.append(GraphicsPath())
        self.start_point = start_point

    # Because the GraphicsPath API works in terms of segments rather than points, it has
    # no equivalent to move_to, and we must save that point manually. In all other
    # situations, we can get the last point from the GraphicsPath itself.
    #
    # default_x and default_y should be set as described in the HTML spec under "ensure
    # there is a subpath".
    def get_last_point(self, default_x, default_y):
        if self.current_path.PointCount:
            return self.current_path.GetLastPoint()
        elif self.start_point:
            return self.start_point
        else:
            return PointF(default_x, default_y)

    def print_path(self, path=None):  # pragma: no cover
        if path is None:
            path = self.current_path
        print(
            "\n".join(
                str((ptype, point.X, point.Y))
                for ptype, point in zip(path.PathTypes, path.PathPoints)
            )
        )


class Canvas(Box):
    def create(self):
        super().create()
        self._default_background_color = TRANSPARENT
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
            width=self.scale_out(self.native.Width),
            height=self.scale_out(self.native.Height),
        )

    def winforms_mouse_down(self, obj, mouse_event):
        x, y = map(self.scale_out, (mouse_event.X, mouse_event.Y))
        if mouse_event.Button == WinForms.MouseButtons.Left:
            if mouse_event.Clicks == 2:
                self.interface.on_activate(x, y)
            else:
                self.interface.on_press(x, y)
                self.dragging = True
        elif mouse_event.Button == WinForms.MouseButtons.Right:
            self.interface.on_alt_press(x, y)
            self.dragging = True
        else:  # pragma: no cover
            pass

    def winforms_mouse_move(self, obj, mouse_event):
        if not self.dragging:
            return
        x, y = map(self.scale_out, (mouse_event.X, mouse_event.Y))
        if mouse_event.Button == WinForms.MouseButtons.Left:
            self.interface.on_drag(x, y)
        elif mouse_event.Button == WinForms.MouseButtons.Right:
            self.interface.on_alt_drag(x, y)
        else:  # pragma: no cover
            pass

    def winforms_mouse_up(self, obj, mouse_event):
        self.dragging = False
        x, y = map(self.scale_out, (mouse_event.X, mouse_event.Y))
        if mouse_event.Button == WinForms.MouseButtons.Left:
            self.interface.on_release(x, y)
        elif mouse_event.Button == WinForms.MouseButtons.Right:
            self.interface.on_alt_release(x, y)
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
        if draw_context.current_path.PointCount:
            start = draw_context.current_path.PathPoints[0]
            draw_context.current_path.AddLine(
                draw_context.current_path.GetLastPoint(), start
            )
            self.move_to(start.X, start.Y, draw_context)

    def move_to(self, x, y, draw_context, **kwargs):
        draw_context.add_path(PointF(x, y))

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
            **kwargs,
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
        **kwargs,
    ):
        matrix = Matrix()
        matrix.Translate(x, y)
        matrix.Rotate(degrees(rotation))
        matrix.Scale(radiusx, radiusy)
        matrix.Rotate(degrees(startangle))

        points = Array[PointF](
            [
                PointF(x, y)
                for x, y in arc_to_bezier(
                    sweepangle(startangle, endangle, anticlockwise)
                )
            ]
        )
        matrix.TransformPoints(points)

        start = draw_context.start_point
        if start and not draw_context.current_path.PointCount:
            draw_context.current_path.AddLine(start, start)
        draw_context.current_path.AddBeziers(points)

    def rect(self, x, y, width, height, draw_context, **kwargs):
        draw_context.add_path()
        rect = RectangleF(x, y, width, height)
        draw_context.current_path.AddRectangle(rect)
        draw_context.add_path()

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
        draw_context.clear_paths()

    def stroke(self, color, line_width, line_dash, draw_context, **kwargs):
        pen = Pen(native_color(color), self.scale_in(line_width, rounding=None))
        if line_dash is not None:
            pen.DashPattern = [ld / line_width for ld in line_dash]

        for path in draw_context.paths:
            path.Transform(draw_context.matrix)
            draw_context.graphics.DrawPath(pen, path)
        draw_context.clear_paths()

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
    def write_text(self, text, x, y, font, baseline, draw_context, line_height_factor = 1.2, **kwargs):
        for op in ["fill", "stroke"]:
            if color := kwargs.pop(f"{op}_color", None):
                self._text_path(text, x, y, font, baseline, draw_context, line_height_factor)
                getattr(self, op)(color, draw_context=draw_context, **kwargs)

    def _text_path(self, text, x, y, font, baseline, draw_context, line_height_factor):
        lines = text.splitlines()
        line_height = font.metric("LineSpacing") * line_height_factor
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

    def measure_text(self, text, font, line_height_factor = 1.2):
        graphics = self.native.CreateGraphics()
        sizes = [
            graphics.MeasureString(line, font.native, 2**31 - 1, self.string_format)
            for line in text.splitlines()
        ]
        return (
            self.scale_out(max(size.Width for size in sizes)),
            font.metric("LineSpacing") * line_height_factor * len(sizes),
        )

    def get_image_data(self):
        # Winforms backgrounds don't honor transparency, so the background that is
        # rendered to screen manually computes the blended color. However, we want the
        # image to reflect the background color that has actually been applied to the
        # image. Temporarily switch out the manually alpha blended background color to
        # the native system produced background color. Suspending the layout means this
        # change isn't visible to the user.
        self.native.SuspendLayout()
        current_background_color = self.interface.style.background_color
        self.native.BackColor = native_color(current_background_color)

        width, height = (self.native.Width, self.native.Height)
        bitmap = Bitmap(width, height)
        rect = Rectangle(0, 0, width, height)
        graphics = Graphics.FromImage(bitmap)
        graphics.Clear(self.native.BackColor)
        self.native.OnPaint(WinForms.PaintEventArgs(graphics, rect))

        stream = MemoryStream()
        bitmap.Save(stream, ImageFormat.Png)

        # Switch back to the manually alpha blended background color, and resume layout
        # updates.
        self.set_background_color(current_background_color)
        self.native.ResumeLayout()

        return bytes(stream.ToArray())
