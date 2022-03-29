import math

from ..libs import activity
from ..libs.android.graphics import DashPathEffect, Matrix, Paint, Paint__Style, Path, Path__Direction
from .base import Widget


class DrawHandler(activity.IDrawHandler):
    def __init__(self, interface):
        self.interface = interface
        super().__init__()

    def handleDraw(self, canvas):
        canvas.save()
        self.interface._draw(self.interface._impl, path=Path(), canvas=canvas)


class Canvas(Widget):
    def create(self):
        # Our native widget is a DrawHandlerView, which delegates drawing to DrawHandler,
        # so we can pass the `android.graphics.Canvas` around as `canvas`.
        self.native = activity.DrawHandlerView(self._native_activity.getApplicationContext())
        self.native.setDrawHandler(DrawHandler(self.interface))

    def redraw(self):
        pass

    def set_on_press(self, handler):
        self.interface.factory.not_implemented('Canvas.set_on_press()')

    def set_on_release(self, handler):
        self.interface.factory.not_implemented('Canvas.set_on_release()')

    def set_on_drag(self, handler):
        self.interface.factory.not_implemented('Canvas.set_on_drag()')

    def set_on_alt_press(self, handler):
        self.interface.factory.not_implemented('Canvas.set_on_alt_press()')

    def set_on_alt_release(self, handler):
        self.interface.factory.not_implemented('Canvas.set_on_alt_release()')

    def set_on_alt_drag(self, handler):
        self.interface.factory.not_implemented('Canvas.set_on_alt_drag()')

    # Basic paths

    def new_path(self, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.new_path()')

    def closed_path(self, x, y, path, *args, **kwargs):
        path.close()

    def move_to(self, x, y, path, *args, **kwargs):
        path.moveTo(self.container.viewport.scale * x, self.container.viewport.scale * y)

    def line_to(self, x, y, path, *args, **kwargs):
        path.lineTo(self.container.viewport.scale * x, self.container.viewport.scale * y)

    # Basic shapes

    def bezier_curve_to(
            self, cp1x, cp1y, cp2x, cp2y, x, y, path, *args, **kwargs
    ):
        path.cubicTo(
            cp1x * self.container.viewport.scale,
            cp1y * self.container.viewport.scale,
            cp2x * self.container.viewport.scale,
            cp2y * self.container.viewport.scale,
            x * self.container.viewport.scale,
            y * self.container.viewport.scale,
        )

    def quadratic_curve_to(self, cpx, cpy, x, y, path, *args, **kwargs):
        path.quadTo(
            cpx * self.container.viewport.scale,
            cpy * self.container.viewport.scale,
            x * self.container.viewport.scale,
            y * self.container.viewport.scale,
        )

    def arc(
            self,
            x,
            y,
            radius,
            startangle,
            endangle,
            anticlockwise,
            path,
            *args,
            **kwargs
    ):
        sweep_angle = endangle - startangle
        if anticlockwise:
            sweep_angle -= math.radians(360)
        path.arcTo(
            self.container.viewport.scale * (x - radius),
            self.container.viewport.scale * (y - radius),
            self.container.viewport.scale * (x + radius),
            self.container.viewport.scale * (y + radius),
            math.degrees(startangle),
            math.degrees(sweep_angle),
            False,
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
        *args,
        **kwargs
    ):
        sweep_angle = endangle - startangle
        if anticlockwise:
            sweep_angle -= math.radians(360)
        ellipse_path = Path()
        ellipse_path.addArc(
            self.container.viewport.scale * (x - radiusx),
            self.container.viewport.scale * (y - radiusy),
            self.container.viewport.scale * (x + radiusx),
            self.container.viewport.scale * (y + radiusy),
            math.degrees(startangle),
            math.degrees(sweep_angle),
        )
        rotation_matrix = Matrix()
        rotation_matrix.postRotate(
            math.degrees(rotation),
            self.container.viewport.scale * x,
            self.container.viewport.scale * y
        )
        ellipse_path.transform(rotation_matrix)
        path.addPath(ellipse_path)

    def rect(self, x, y, width, height, path, *args, **kwargs):
        path.addRect(
            self.container.viewport.scale * x,
            self.container.viewport.scale * y,
            self.container.viewport.scale * (x + width),
            self.container.viewport.scale * (y + height),
            Path__Direction.CW,
        )

    # Drawing Paths

    def fill(self, color, fill_rule, preserve, path, canvas, *args, **kwargs):
        draw_paint = Paint()
        draw_paint.setAntiAlias(True)
        draw_paint.setStyle(Paint__Style.FILL)
        if color is None:
            a, r, g, b = 255, 0, 0, 0
        else:
            a, r, g, b = round(color.a * 255), int(color.r), int(color.g), int(color.b)
        draw_paint.setARGB(a, r, g, b)

        canvas.drawPath(path, draw_paint)
        path.reset()

    def stroke(self, color, line_width, line_dash, path, canvas, *args, **kwargs):
        draw_paint = Paint()
        draw_paint.setAntiAlias(True)
        draw_paint.setStrokeWidth(self.container.viewport.scale * line_width)
        draw_paint.setStyle(Paint__Style.STROKE)
        if color is None:
            a, r, g, b = 255, 0, 0, 0
        else:
            a, r, g, b = round(color.a * 255), int(color.r), int(color.g), int(color.b)
        if line_dash is not None:
            draw_paint.setPathEffect(DashPathEffect(
                [(self.container.viewport.scale * float(d)) for d in line_dash], 0.0))
        draw_paint.setARGB(a, r, g, b)

        canvas.drawPath(path, draw_paint)
        path.reset()

    # Transformations

    def rotate(self, radians, canvas, *args, **kwargs):
        canvas.rotate(math.degrees(radians))

    def scale(self, sx, sy, canvas, *args, **kwargs):
        canvas.scale(float(sx), float(sy))

    def translate(self, tx, ty, canvas, *args, **kwargs):
        canvas.translate(self.container.viewport.scale * tx, self.container.viewport.scale * ty)

    def reset_transform(self, canvas, *args, **kwargs):
        canvas.restore()
        canvas.save()

    # Text

    def measure_text(self, text, font, tight=False):
        self.interface.factory.not_implemented('Canvas.measure_text')

    def write_text(self, text, x, y, font, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.write_text')

    # Rehint

    def set_on_resize(self, handler):
        self.interface.factory.not_implemented('Canvas.on_resize')
