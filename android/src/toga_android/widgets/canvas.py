import itertools
import weakref
from copy import deepcopy
from math import degrees
from typing import NamedTuple

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

from toga.colors import rgb
from toga.constants import Baseline, FillRule
from toga.widgets.canvas import arc_to_bezier, sweepangle

from ..colors import native_color
from .base import Widget, suppress_reference_error

BLACK = jint(native_color(rgb(0, 0, 0)))


class State(NamedTuple):
    fill: Paint
    stroke: Paint

    def __deepcopy__(self, memo):
        return type(self)(Paint(self.fill), Paint(self.stroke))


class Context:
    def __init__(self, impl, native):
        self.native = native
        self.impl = impl
        self.path = Path()
        self.reset_transform()

        # Backwards compatibility for Toga <= 0.5.3
        self.in_fill = False
        self.in_stroke = False

        fill = Paint()
        fill.setAntiAlias(True)
        fill.setStyle(Paint.Style.FILL)
        fill.setColor(BLACK)

        stroke = Paint()
        stroke.setAntiAlias(True)
        stroke.setStyle(Paint.Style.STROKE)
        stroke.setStrokeWidth(2.0)
        stroke.setColor(BLACK)

        self.states = [State(fill, stroke)]

    @property
    def state(self):
        return self.states[-1]

    # Context management

    def save(self):
        self.native.save()
        self.states.append(deepcopy(self.state))

    def restore(self):
        self.native.restore()
        self.states.pop()

    # Setting attributes
    def set_fill_style(self, color):
        self.state.fill.setColor(jint(native_color(color)))

    def set_line_dash(self, line_dash):
        self.state.stroke.setPathEffect(DashPathEffect(line_dash, 0))

    def set_line_width(self, line_width):
        self.state.stroke.setStrokeWidth(line_width)

    def set_stroke_style(self, color):
        self.state.stroke.setColor(jint(native_color(color)))

    # Basic paths

    def begin_path(self):
        self.path.reset()

    def close_path(self):
        self.path.close()

    def move_to(self, x, y):
        self.path.moveTo(x, y)

    def line_to(self, x, y):
        self._ensure_subpath(x, y)
        self.path.lineTo(x, y)

    def _ensure_subpath(self, x, y):
        if self.path.isEmpty():
            self.move_to(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self._ensure_subpath(cp1x, cp1y)
        self.path.cubicTo(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self._ensure_subpath(cpx, cpy)
        self.path.quadTo(cpx, cpy, x, y)

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
        matrix.preTranslate(x, y)
        matrix.preRotate(degrees(rotation))
        matrix.preScale(radiusx, radiusy)
        matrix.preRotate(degrees(startangle))

        coords = list(
            itertools.chain(
                *arc_to_bezier(sweepangle(startangle, endangle, counterclockwise))
            )
        )
        matrix.mapPoints(coords)

        self.line_to(coords[0], coords[1])
        i = 2
        while i < len(coords):
            self.bezier_curve_to(*coords[i : i + 6])
            i += 6

    def rect(self, x, y, width, height):
        self.path.addRect(x, y, x + width, y + height, Path.Direction.CW)

    # Drawing Paths

    def fill(self, fill_rule):
        self.path.setFillType(
            {
                FillRule.EVENODD: Path.FillType.EVEN_ODD,
                FillRule.NONZERO: Path.FillType.WINDING,
            }.get(fill_rule, Path.FillType.WINDING)
        )
        self.native.drawPath(self.path, self.state.fill)

    def stroke(self):
        # The stroke respects the canvas transform, so we don't need to scale it here.
        self.native.drawPath(self.path, self.state.stroke)

    # Transformations

    def rotate(self, radians):
        self.native.rotate(degrees(radians))

    def scale(self, sx, sy):
        self.native.scale(sx, sy)

    def translate(self, tx, ty):
        self.native.translate(tx, ty)

    def reset_transform(self):
        self.native.setMatrix(None)
        self.scale(self.impl.dpi_scale, self.impl.dpi_scale)

    # Text
    def write_text(self, text, x, y, font, baseline, line_height):
        lines = text.splitlines()
        paint = self.impl._text_paint(font)
        scaled_line_height = self.impl._line_height(paint, line_height)
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

        # Avoid mutating state
        if self.in_fill:
            fill = Paint(self.state.fill)
            fill.setTypeface(font.typeface())
            fill.setTextSize(self.impl.scale_out(font.size()))

        if self.in_stroke:
            stroke = Paint(self.state.stroke)
            stroke.setTypeface(font.typeface())
            stroke.setTextSize(self.impl.scale_out(font.size()))

        for line_num, line in enumerate(text.splitlines()):
            # FILL_AND_STROKE doesn't allow separate colors, so we have to draw twice.
            draw_args = (line, x, top + (scaled_line_height * line_num))

            if self.in_fill:
                self.native.drawText(*draw_args, fill)
            if self.in_stroke:
                self.native.drawText(*draw_args, stroke)

    # Bitmaps
    def draw_image(self, image, x, y, width, height):
        self.native.save()
        self.native.translate(x, y)
        self.native.scale(width / image.width, height / image.height)
        self.native.drawBitmap(
            image._impl.native,
            0,
            0,
            None,
        )
        self.native.restore()


class DrawHandler(dynamic_proxy(IDrawHandler)):
    def __init__(self, impl):
        super().__init__()
        self.impl = weakref.proxy(impl)
        self.interface = weakref.proxy(impl.interface)

    def handleDraw(self, canvas):
        with suppress_reference_error():
            context = Context(self.impl, canvas)
            self.interface.context._draw(context)


class TouchListener(dynamic_proxy(View.OnTouchListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = weakref.proxy(impl)
        self.interface = weakref.proxy(impl.interface)

    def onTouch(self, canvas, event):
        with suppress_reference_error():
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

    def measure_text(self, text, font, line_height):
        paint = self._text_paint(font)
        sizes = [paint.measureText(line) for line in text.splitlines()]
        return (
            max(sizes),
            self._line_height(paint, line_height) * len(sizes),
        )

    def _line_height(self, paint, line_height):
        if line_height is None:
            return paint.getFontSpacing()
        else:
            return paint.getTextSize() * line_height

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
