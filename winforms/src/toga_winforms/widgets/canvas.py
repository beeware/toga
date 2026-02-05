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

from toga.colors import TRANSPARENT, rgb
from toga.constants import Baseline, FillRule
from toga.handlers import WeakrefCallable
from toga.widgets.canvas.geometry import arc_to_bezier, round_rect, sweepangle
from toga_winforms.colors import native_color

from .box import Box

BLACK = native_color(rgb(0, 0, 0))


class Path2D:
    def __init__(self, path=None):
        if path is None:
            self.native = GraphicsPath()
            self._subpath_start = None
            self._subpath_end = None
            self._subpath_empty = True
        else:
            self.native = GraphicsPath(path.native.PathPoints, path.native.PathTypes)
            self._subpath_start = path._subpath_start
            self._subpath_end = path._subpath_end
            self._subpath_empty = path._subpath_empty

    def _ensure_path(self, x, y):
        if self._subpath_start is None:
            self.move_to(x, y)

    @property
    def last_point(self):
        return self._subpath_end

    def add_path(self, path, transform=None):
        if transform is None:
            self.native.AddPath(path.native)
            self._subpath_end = path._subpath_end
        else:
            native_path = GraphicsPath(path.native.PathPoints, path.native.PathTypes)
            matrix = Matrix(*transform)
            native_path.Transform(matrix)
            self.native.AddPath(native_path, False)
            if self._subpath_start is None and path._subpath_start is not None:
                points = Array[PointF]([path._subpath_start])
                matrix.TransformPoints(points)
                self._subpath_start = points[0]
            if path._subpath_end is not None:
                points = Array[PointF]([path._subpath_end])
                matrix.TransformPoints(points)
                self._subpath_end = points[0]

    def close_path(self):
        if self._subpath_start is not None:
            # We don't use current_path.CloseFigure, because that causes the dash
            # pattern to start on the last segment of the path rather than the first
            # one.
            self.line_to(self._subpath_start.X, self._subpath_start.Y)
        self._subpath_end = self._subpath_start

    def move_to(self, x, y):
        self._subpath_end = PointF(x, y)
        self._subpath_start = self._subpath_end
        if not self._subpath_empty:
            self.native.StartFigure()
            self._subpath_empty = True

    def line_to(self, x, y):
        self._ensure_path(x, y)
        self.native.AddLine(self.last_point, PointF(x, y))
        self._subpath_end = PointF(x, y)
        self._subpath_empty = False

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self._ensure_path(cp1x, cp1y)
        self.native.AddBezier(
            self.last_point,
            PointF(cp1x, cp1y),
            PointF(cp2x, cp2y),
            PointF(x, y),
        )
        self._subpath_end = PointF(x, y)
        self._subpath_empty = False

    def quadratic_curve_to(self, cpx, cpy, x, y):
        # A Quadratic curve is a dimensionally reduced Bézier Cubic curve;
        # we can convert the single Quadratic control point into the
        # 2 control points required for the cubic Bézier.
        self._ensure_path(cpx, cpy)
        x0, y0 = (self.last_point.X, self.last_point.Y)
        self.native.AddBezier(
            self.last_point,
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
        self._subpath_end = PointF(x, y)
        self._subpath_empty = False

    def arc(self, x, y, radius, startangle, endangle, counterclockwise):
        self.ellipse(x, y, radius, radius, 0, startangle, endangle, counterclockwise)

    def ellipse(
        self,
        x,
        y,
        radiusx,
        radiusy,
        rotation,
        startangle,
        endangle,
        counterclockwise,
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
                    sweepangle(startangle, endangle, counterclockwise)
                )
            ]
        )
        matrix.TransformPoints(points)

        self._ensure_path(points[0].X, points[0].Y)
        self.native.AddLine(PointF(self._subpath_end.X, self._subpath_end.Y), points[0])
        self.native.AddBeziers(points)
        self._subpath_end = points[-1]
        self._subpath_empty = False

    def rect(self, x, y, width, height):
        rect = RectangleF(x, y, width, height)
        self.native.AddRectangle(rect)
        if self._subpath_start is None:
            self._subpath_start = PointF(x, y)
        self._subpath_end = PointF(x, y)
        self._subpath_empty = False

    def round_rect(self, x, y, width, height, radii):
        set_start = self._subpath_start is None
        round_rect(self, x, y, width, height, radii)
        if set_start:
            self._subpath_start = PointF(x, y)
        self._subpath_end = PointF(x, y)
        self._subpath_empty = False


class State:
    """Represents a canvas state; can be saved and restored.

    WinForms has its own GraphicsState, which can track transformation, but it doesn't
    manage fill or stroke styles, so we'd still have to handle those ourselves even if
    we used it. And it would still need to be kept in a list.
    """

    def __init__(self, previous_state, brush, pen, singular=False):
        # This is the previous graphics state, so we can restore.
        self.previous_state = previous_state
        self.brush = brush
        self.pen = pen
        # When we are in a singular state, should not draw anything
        self.singular = singular
        self.transform = Matrix()

    @classmethod
    def for_impl(cls, impl):
        return cls(
            previous_state=None,
            brush=SolidBrush(BLACK),
            pen=Pen(BLACK, impl.scale_in(2.0, rounding=None)),
        )

    def new_state(self, previous_state):
        return type(self)(
            previous_state=previous_state,
            brush=self.brush.Clone(),
            pen=self.pen.Clone(),
            singular=self.singular,
        )


class Context:
    def __init__(self, impl, native):
        self.native = native
        self.native.PixelOffsetMode = PixelOffsetMode.HighQuality
        self.native.SmoothingMode = SmoothingMode.AntiAlias
        self.begin_path()
        self.impl = impl
        self.states = [State.for_impl(self.impl)]

        # Backwards compatibility for Toga <= 0.5.3
        self.in_fill = False
        self.in_stroke = False

    # Windows path management
    def transform_path(self, matrix):
        """Transform the current path using a matrix."""
        self.path.native.Transform(matrix)
        if (start := self.path._subpath_start) is not None:
            points = Array[PointF]([start])
            matrix.TransformPoints(points)
            self.path._subpath_start = points[0]
        if (end := self.path._subpath_end) is not None:
            points = Array[PointF]([end])
            matrix.TransformPoints(points)
            self.path._subpath_end = points[0]

    # Context management

    @property
    def state(self):
        return self.states[-1]

    def save(self):
        graphics_state = self.native.Save()
        self.states.append(self.state.new_state(graphics_state))

    def restore(self):
        state = self.states.pop()
        self.native.Restore(state.previous_state)
        self.transform_path(state.transform)

    # Setting attributes

    def set_fill_style(self, color):
        self.state.brush.Color = native_color(color)

    def set_line_dash(self, line_dash):
        self.state.pen.DashPattern = [ld / self.state.pen.Width for ld in line_dash]

    def set_line_width(self, line_width):
        self.state.pen.Width = line_width

    def set_stroke_style(self, color):
        self.state.pen.Color = native_color(color)

    # Basic paths

    def begin_path(self):
        self.path = Path2D()

    def close_path(self):
        self.path.close_path()

    def move_to(self, x, y):
        self.path.move_to(x, y)

    def line_to(self, x, y):
        self.path.line_to(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.path.bezier_curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self.path.quadratic_curve_to(cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, counterclockwise):
        self.path.arc(x, y, radius, startangle, endangle, counterclockwise)

    def ellipse(
        self,
        x,
        y,
        radiusx,
        radiusy,
        rotation,
        startangle,
        endangle,
        counterclockwise,
    ):
        self.path.ellipse(
            x,
            y,
            radiusx,
            radiusy,
            rotation,
            startangle,
            endangle,
            counterclockwise,
        )

    def rect(self, x, y, width, height):
        self.path.rect(x, y, width, height)

    def round_rect(self, x, y, width, height, radii):
        self.path.round_rect(x, y, width, height, radii)

    # Drawing Paths

    def fill(self, fill_rule, path=None):
        if self.state.singular:
            # draw nothing
            return
        if path is None:
            path = self.path

        if fill_rule == FillRule.EVENODD:
            path.native.FillMode = FillMode.Alternate
        else:  # Default to NONZERO
            path.native.FillMode = FillMode.Winding
        self.native.FillPath(self.state.brush, path.native)

    def stroke(self, path=None):
        if self.state.singular:
            # draw nothing
            return
        if path is None:
            path = self.path
        self.native.DrawPath(self.state.pen, path.native)

    # Transformations

    def rotate(self, radians):
        self.native.RotateTransform(degrees(radians))

        # Update state transform
        self.state.transform.Rotate(degrees(radians))

        # Transform active path to current coordinates
        inverse = Matrix()
        inverse.Rotate(-degrees(radians))
        self.transform_path(inverse)

    def scale(self, sx, sy):
        # Can't apply inverse transform if scale is 0,
        # so use a small epsilon which will almost be the same
        if sx == 0:
            sx = 2**-24
            self.state.singular = True
        if sy == 0:
            sy = 2**-24
            self.state.singular = True

        self.native.ScaleTransform(sx, sy)

        # Update state transform
        self.state.transform.Scale(sx, sy)

        # Transform active path to current coordinates
        inverse = Matrix()
        inverse.Scale(1 / sx, 1 / sy)
        self.transform_path(inverse)

    def translate(self, tx, ty):
        self.native.TranslateTransform(tx, ty)

        # Update state transform
        self.state.transform.Translate(tx, ty)

        # Transform active path to current coordinates
        inverse = Matrix()
        inverse.Translate(-tx, -ty)
        self.transform_path(inverse)

    def reset_transform(self):
        matrix = self.native.Transform
        self.native.ResetTransform()

        # Transform active path to current coordinates
        self.transform_path(matrix)

        # Update state transform
        matrix.Invert()
        self.state.transform.Multiply(matrix)

        self.state.singular = False
        self.scale(self.impl.dpi_scale, self.impl.dpi_scale)

    # Text

    def write_text(self, text, x, y, font, baseline, line_height):
        # Writing text should not affect current path, so create a separate path
        path = self._text_path(text, x, y, font, baseline, line_height)
        if self.in_fill:
            self.fill(FillRule.NONZERO, path)
        if self.in_stroke:
            self.stroke(path)

    def _text_path(self, text, x, y, font, baseline, line_height):
        lines = text.splitlines()
        scaled_line_height = self.impl._line_height(font, line_height)
        total_height = scaled_line_height * len(lines)

        if baseline == Baseline.TOP:
            top = y
        elif baseline == Baseline.MIDDLE:
            top = y - (total_height / 2)
        elif baseline == Baseline.BOTTOM:
            top = y - total_height
        else:
            # Default to Baseline.ALPHABETIC
            top = y - font.metric("CellAscent")

        path = Path2D()
        for line_num, line in enumerate(lines):
            path.native.AddString(
                line,
                font.native.FontFamily,
                font.native.Style.value__,
                font.metric("EmHeight"),
                PointF(x, top + (scaled_line_height * line_num)),
                self.impl.string_format,
            )
        return path

    def draw_image(self, image, x, y, width, height):
        self.native.DrawImage(image._impl.native, x, y, width, height)


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

    # The control automatically paints the background color, so painting it again here
    # would give incorrect results if it was semi-transparent. But we do paint it in
    # get_image_data.
    def winforms_paint(self, panel, event, *args):
        context = Context(self, event.Graphics)
        self.interface.root_state._draw(context)

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

    # Text
    def _line_height(self, font, line_height):
        if line_height is None:
            return font.metric("LineSpacing")
        else:
            # Get size in CSS pixels
            return (font.native.SizeInPoints * 96 / 72) * line_height

    def measure_text(self, text, font, line_height):
        graphics = self.native.CreateGraphics()
        sizes = [
            graphics.MeasureString(line, font.native, 2**31 - 1, self.string_format)
            for line in text.splitlines()
        ]
        return (
            self.scale_out(max(size.Width for size in sizes)),
            self._line_height(font, line_height) * len(sizes),
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
