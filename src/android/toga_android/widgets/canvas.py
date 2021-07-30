from ..libs import activity
from ..libs.android.graphics import Paint, Paint__Style, Path
from .base import Widget

# Arbitrary scale factor; to be made more specific in the future.
SCALE_FACTOR = 5


class DrawHandler(activity.IDrawHandler):
    def __init__(self, interface):
        self.interface = interface
        super().__init__()

    def handleDraw(self, canvas):
        self.interface._draw(self.interface._impl, draw_context=canvas)


class Canvas(Widget):
    def create(self):
        # Our native widget is a DrawHandlerView, which delegates drawing to DrawHandler,
        # so we can pass the `android.graphics.Canvas` around as `draw_context`.
        self.native = activity.DrawHandlerView(self._native_activity.getApplicationContext())
        self.native.setDrawHandler(DrawHandler(self.interface))
        self._path = None
        self._draw_paint = None

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

    def new_path(self, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.new_path()')

    def closed_path(self, x, y, draw_context, *args, **kwargs):
        pass

    def move_to(self, x, y, draw_context, *args, **kwargs):
        self._path = Path()
        self._path.moveTo(float(x) * SCALE_FACTOR, float(y) * SCALE_FACTOR)

    def line_to(self, x, y, draw_context, *args, **kwargs):
        self._path.lineTo(float(x) * SCALE_FACTOR, float(y) * SCALE_FACTOR)

    # Basic shapes

    def bezier_curve_to(
            self, cp1x, cp1y, cp2x, cp2y, x, y, draw_context, *args, **kwargs
    ):
        self.interface.factory.not_implemented('Canvas.bezier_curve_to()')

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.quadratic_curve_to()')

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
        self.interface.factory.not_implemented('Canvas.arc()')

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
        **kwargs
    ):
        self.interface.factory.not_implemented('Canvas.ellipse')

    def rect(self, x, y, width, height, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.rect')

    # Drawing Paths

    def fill(self, color, fill_rule, preserve, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.fill()')

    def stroke(self, color, line_width, line_dash, draw_context, *args, **kwargs):
        self._draw_paint = Paint()
        self._draw_paint.setAntiAlias(True)
        self._draw_paint.setStrokeWidth(float(line_width) * SCALE_FACTOR)
        self._draw_paint.setStyle(Paint__Style.STROKE)
        if color is None:
            a, r, g, b = 255, 0, 0, 0
        else:
            a, r, g, b = round(color.a * 255), int(color.r), int(color.g), int(color.b)
        self._draw_paint.setARGB(a, r, g, b)

        draw_context.drawPath(self._path, self._draw_paint)

    # Transformations

    def rotate(self, radians, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.rotate')

    def scale(self, sx, sy, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.scale')

    def translate(self, tx, ty, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.translate')

    def reset_transform(self, draw_context, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.reset_transform')

    # Text

    def measure_text(self, text, font, tight=False):
        self.interface.factory.not_implemented('Canvas.measure_text')

    def write_text(self, text, x, y, font, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.write_text')

    # Rehint

    def set_on_resize(self, handler):
        self.interface.factory.not_implemented('Canvas.on_resize')
