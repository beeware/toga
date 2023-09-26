from math import degrees, pi

from java import dynamic_proxy, jint
from java.io import ByteArrayOutputStream
from org.beeware.android import DrawHandlerView, IDrawHandler
from travertino.size import at_least

from android.graphics import (
    Bitmap,
    Canvas as A_Canvas,
    DashPathEffect,
    Matrix,
    Paint,
    Path,
)

from ..colors import native_color
from .base import Widget


class DrawHandler(dynamic_proxy(IDrawHandler)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def handleDraw(self, canvas):
        self.impl.reset_transform(canvas)
        self.impl.interface.context._draw(self.impl, path=Path(), canvas=canvas)


class Canvas(Widget):
    def create(self):
        self.native = DrawHandlerView(self._native_activity)
        self.native.setDrawHandler(DrawHandler(self))

    def redraw(self):
        self.native.invalidate()

    # Context management

    def push_context(self, canvas, **kwargs):
        canvas.save()

    def pop_context(self, canvas, **kwargs):
        canvas.restore()

    # Basic paths

    def begin_path(self, path, **kwargs):
        path.reset()

    def close_path(self, path, **kwargs):
        path.close()

    def move_to(self, x, y, path, **kwargs):
        path.moveTo(x, y)

    def line_to(self, x, y, path, **kwargs):
        path.lineTo(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, path, **kwargs):
        path.cubicTo(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, path, **kwargs):
        path.quadTo(cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, path, **kwargs):
        sweepangle = endangle - startangle
        if anticlockwise:
            if sweepangle > 0:
                sweepangle -= 2 * pi
        else:
            if sweepangle < 0:
                sweepangle += 2 * pi

        # HTML says sweep angles should be clamped at +/- 360 degrees, but Android uses
        # mod 360 instead, so 360 would cause the circle to completely disappear.
        limit = 359.999  # Must be less than 360 in 32-bit floating point.
        path.arcTo(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            degrees(startangle),
            max(-limit, min(degrees(sweepangle), limit)),
            False,  # forceMoveTo
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
        path,
        **kwargs,
    ):
        matrix = Matrix()
        matrix.postScale(radiusx, radiusy)
        matrix.postRotate(degrees(rotation))
        matrix.postTranslate(x, y)

        # Creating the ellipse as a separate path and then using addPath would make it a
        # disconnected contour. And there's no way to extract the segments from a path
        # until getPathIterator in API level 34. So this is the simplest solution I
        # could find.
        inverse = Matrix()
        matrix.invert(inverse)
        path.transform(inverse)
        self.arc(0, 0, 1, startangle, endangle, anticlockwise, path)
        path.transform(matrix)

    def rect(self, x, y, width, height, path, **kwargs):
        path.addRect(x, y, x + width, y + height, Path.Direction.CW)

    # Drawing Paths

    def fill(self, color, fill_rule, path, canvas, **kwargs):
        draw_paint = Paint()
        draw_paint.setAntiAlias(True)
        draw_paint.setStyle(Paint.Style.FILL)
        draw_paint.setColor(jint(native_color(color)))

        canvas.drawPath(path, draw_paint)
        path.reset()

    def stroke(self, color, line_width, line_dash, path, canvas, **kwargs):
        draw_paint = Paint()
        draw_paint.setAntiAlias(True)
        draw_paint.setStyle(Paint.Style.STROKE)
        draw_paint.setColor(jint(native_color(color)))

        # The stroke respects the canvas transform, so we don't need to scale it here.
        draw_paint.setStrokeWidth(line_width)
        if line_dash is not None:
            draw_paint.setPathEffect(DashPathEffect(line_dash, 0))

        canvas.drawPath(path, draw_paint)
        path.reset()

    # Transformations

    def rotate(self, radians, canvas, **kwargs):
        canvas.rotate(degrees(radians))

    def scale(self, sx, sy, canvas, **kwargs):
        canvas.scale(sx, sy)

    def translate(self, tx, ty, canvas, **kwargs):
        canvas.translate(tx, ty)

    def reset_transform(self, canvas, **kwargs):
        canvas.setMatrix(None)
        self.scale(self.dpi_scale, self.dpi_scale, canvas)

    # Text

    def measure_text(self, text, font):
        self.interface.factory.not_implemented("Canvas.measure_text")
        return (10, 10)

    def write_text(self, text, x, y, font, **kwargs):
        self.interface.factory.not_implemented("Canvas.write_text")

    def get_image_data(self):
        bitmap = Bitmap.createBitmap(
            self.native.getWidth(), self.native.getHeight(), Bitmap.Config.ARGB_8888
        )
        canvas = A_Canvas(bitmap)
        self.native.getBackground().draw(canvas)
        self.native.draw(canvas)

        stream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.PNG, 0, stream)
        return bytes(stream.toByteArray())

    def set_background_color(self, value):
        self.set_background_simple(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
