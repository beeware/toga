import itertools
from math import degrees

from android.graphics import (
    Bitmap,
    Canvas as A_Canvas,
    DashPathEffect,
    Matrix,
    Paint,
    Path,
)
from android.view import MotionEvent, View
from java import dynamic_proxy, jint
from java.io import ByteArrayOutputStream
from org.beeware.android import DrawHandlerView, IDrawHandler

from toga.constants import Baseline, FillRule
from toga.widgets.canvas import arc_to_bezier, sweepangle

from ..colors import native_color
from .base import Widget


class DrawHandler(dynamic_proxy(IDrawHandler)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface

    def handleDraw(self, canvas):
        self.impl.reset_transform(canvas)
        self.interface.context._draw(self.impl, path=Path(), canvas=canvas)


class TouchListener(dynamic_proxy(View.OnTouchListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface

    def onTouch(self, canvas, event):
        x, y = map(self.impl.scale_out, (event.getX(), event.getY()))
        if (action := event.getAction()) == MotionEvent.ACTION_DOWN:
            self.interface.on_press(x, y)
        elif action == MotionEvent.ACTION_MOVE:
            self.interface.on_drag(x, y)
        elif action == MotionEvent.ACTION_UP:
            self.interface.on_release(x, y)
        else:  # pragma: no cover
            return False
        return True


class Canvas(Widget):
    def create(self):
        self.native = DrawHandlerView(self._native_activity)
        self.native.setDrawHandler(DrawHandler(self))
        self.native.setOnTouchListener(TouchListener(self))

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.interface.on_resize(width=width, height=height)

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
        self._ensure_subpath(x, y, path)
        path.lineTo(x, y)

    def _ensure_subpath(self, x, y, path):
        if path.isEmpty():
            self.move_to(x, y, path)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, path, **kwargs):
        self._ensure_subpath(cp1x, cp1y, path)
        path.cubicTo(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, path, **kwargs):
        self._ensure_subpath(cpx, cpy, path)
        path.quadTo(cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, path, **kwargs):
        self.ellipse(
            x, y, radius, radius, 0, startangle, endangle, anticlockwise, path, **kwargs
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
        matrix.preTranslate(x, y)
        matrix.preRotate(degrees(rotation))
        matrix.preScale(radiusx, radiusy)
        matrix.preRotate(degrees(startangle))

        coords = list(
            itertools.chain(
                *arc_to_bezier(sweepangle(startangle, endangle, anticlockwise))
            )
        )
        matrix.mapPoints(coords)

        self.line_to(coords[0], coords[1], path, **kwargs)
        i = 2
        while i < len(coords):
            self.bezier_curve_to(*coords[i : i + 6], path, **kwargs)
            i += 6

    def rect(self, x, y, width, height, path, **kwargs):
        path.addRect(x, y, x + width, y + height, Path.Direction.CW)

    # Drawing Paths

    def fill(self, color, fill_rule, path, canvas, **kwargs):
        draw_paint = Paint()
        draw_paint.setAntiAlias(True)
        draw_paint.setStyle(Paint.Style.FILL)
        draw_paint.setColor(jint(native_color(color)))

        path.setFillType(
            {
                FillRule.EVENODD: Path.FillType.EVEN_ODD,
                FillRule.NONZERO: Path.FillType.WINDING,
            }.get(fill_rule, Path.FillType.WINDING)
        )
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

    def measure_text(self, text, font, line_height):
        paint = self._text_paint(font)
        sizes = [paint.measureText(line) for line in text.splitlines()]
        return (
            max(size for size in sizes),
            paint.getFontSpacing() * len(sizes) * line_height,
        )

    def write_text(self, text, x, y, font, baseline, line_height, canvas, **kwargs):
        lines = text.splitlines()
        paint = self._text_paint(font)
        scaled_line_height = paint.getFontSpacing() * line_height
        total_height = scaled_line_height * len(lines)

        # paint.ascent returns a negative number.
        if baseline == Baseline.TOP:
            top = y - paint.ascent()
        elif baseline == Baseline.MIDDLE:
            top = y - paint.ascent() - (total_height / 2)
        elif baseline == Baseline.BOTTOM:
            top = y - paint.ascent() - total_height
        else:
            # Default to Baseline.ALPHABETIC
            top = y

        for line_num, line in enumerate(text.splitlines()):
            # FILL_AND_STROKE doesn't allow separate colors, so we have to draw twice.
            def draw():
                canvas.drawText(line, x, top + (scaled_line_height * line_num), paint)

            if (color := kwargs.get("fill_color")) is not None:
                paint.setStyle(Paint.Style.FILL)
                paint.setColor(jint(native_color(color)))
                draw()
            if (color := kwargs.get("stroke_color")) is not None:
                paint.setStyle(Paint.Style.STROKE)
                paint.setStrokeWidth(kwargs["line_width"])
                paint.setColor(jint(native_color(color)))
                draw()

    def _text_paint(self, font):
        # font.size applies the scale factor, and the canvas transformation matrix
        # will apply it again, so we need to cancel one of those with a scale_out.
        paint = Paint()
        paint.setTypeface(font.typeface())
        paint.setTextSize(self.scale_out(font.size()))
        return paint

    def get_image_data(self):
        bitmap = Bitmap.createBitmap(
            self.native.getWidth(), self.native.getHeight(), Bitmap.Config.ARGB_8888
        )
        canvas = A_Canvas(bitmap)
        background = self.native.getBackground()
        if background:
            background.draw(canvas)
        self.native.draw(canvas)

        stream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.PNG, 0, stream)
        return bytes(stream.toByteArray())

    def set_background_color(self, value):
        self.set_background_simple(value)
