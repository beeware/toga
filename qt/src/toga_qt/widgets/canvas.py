from math import ceil, cos, degrees, sin

from PySide6.QtCore import QBuffer, QIODevice, Qt
from PySide6.QtGui import QFontMetrics, QPainter, QPainterPath, QPaintEvent, QPen
from PySide6.QtWidgets import QWidget
from travertino.size import at_least

from toga.constants import Baseline, FillRule

from ..colors import native_color
from .base import Widget


class TogaCanvas(QWidget):
    def __init__(self, interface, impl):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.interface = interface
        self.impl = impl

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.impl.begin_path(painter)
        self.interface.context._draw(self.impl, draw_context=painter)


class Canvas(Widget):
    _path: QPainterPath

    def create(self):
        self.native = TogaCanvas(self.interface, self)

    def redraw(self):
        self.native.update()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.interface.on_resize(width=width, height=height)

    def set_background_color(self, color):
        palette = self.native.palette()
        palette.setColor(self.native.backgroundRole(), native_color(color))
        self.native.setPalette(palette)

    # Context management
    def push_context(self, draw_context: QPainter, **kwargs):
        draw_context.save()

    def pop_context(self, draw_context: QPainter, **kwargs):
        draw_context.restore()

    # Basic paths
    def begin_path(self, draw_context: QPainter, **kwargs):
        self._path = QPainterPath()

    def close_path(self, draw_context: QPainter, **kwargs):
        self._path.closeSubpath()

    def move_to(self, x, y, draw_context: QPainter, **kwargs):
        self._path.moveTo(x, y)

    def line_to(self, x, y, draw_context, **kwargs):
        self._path.lineTo(x, y)

    # Basic shapes

    def bezier_curve_to(
        self,
        cp1x,
        cp1y,
        cp2x,
        cp2y,
        x,
        y,
        draw_context,
        **kwargs,
    ):
        self._path.cubicTo(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, **kwargs):
        self._path.quadTo(cpx, cpy, x, y)

    def arc(
        self,
        x,
        y,
        radius,
        startangle,
        endangle,
        counterclockwise,
        draw_context,
        **kwargs,
    ):
        # Qt measures angles counterclockwise from x-axis; Toga measures clockwise
        sweep_angle_counterclockwise = (
            endangle - startangle if counterclockwise else startangle - endangle
        )
        if self._path.isEmpty():
            # if this is the first point of the path, don't draw a line
            # to the start point
            self._path.moveTo(
                x + radius * cos(startangle),
                y + radius * sin(startangle),
            )
        self._path.arcTo(
            x - radius,
            y - radius,
            radius * 2,
            radius * 2,
            -degrees(startangle),
            degrees(sweep_angle_counterclockwise),
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
        counterclockwise,
        draw_context: QPainter,
        **kwargs,
    ):
        # Qt measures angles counterclockwise from x-axis; Toga measures clockwise
        sweep_angle_counterclockwise = (
            endangle - startangle if counterclockwise else startangle - endangle
        )
        # handle rotation by translating center to origin and rotating
        if self._path.isEmpty():
            # if this is the first point of the path, don't draw a line
            # to the start point
            self._path.moveTo(
                x + radiusx * cos(startangle),
                y + radiusy * sin(startangle),
            )
        self._path.arcTo(
            x - radiusx,
            y - radiusy,
            radiusx * 2,
            radiusy * 2,
            -degrees(startangle),
            degrees(sweep_angle_counterclockwise),
        )

    def rect(self, x, y, width, height, draw_context, **kwargs):
        self._path.addRect(x, y, width, height)

    # Drawing Paths

    def fill(self, color, fill_rule, draw_context: QPainter, **kwargs):
        if fill_rule == FillRule.EVENODD:
            self._path.setFillRule(Qt.FillRule.OddEvenFill)
        else:
            self._path.setFillRule(Qt.FillRule.WindingFill)
        draw_context.fillPath(self._path, native_color(color))
        self.begin_path(draw_context)

    def stroke(self, color, line_width, line_dash, draw_context, **kwargs):
        pen = QPen(native_color(color))
        pen.setWidth(line_width)
        if line_dash is not None:
            pen.setDashPattern(line_dash)
        draw_context.strokePath(self._path, pen)
        self.begin_path(draw_context)

    # Transformations
    def rotate(self, radians, draw_context: QPainter, **kwargs):
        draw_context.rotate(radians)

    def scale(self, sx, sy, draw_context: QPainter, **kwargs):
        draw_context.scale(sx, sy)

    def translate(self, tx, ty, draw_context: QPainter, **kwargs):
        draw_context.translate(tx, ty)

    def reset_transform(self, draw_context: QPainter, **kwargs):
        draw_context.resetTransform()

    # Text
    def measure_text(self, text, font, line_height):
        metrics = QFontMetrics(font.native)
        if line_height is None:
            line_height = metrics.lineSpacing()
        else:
            line_height *= font.native.pointSize()
        sizes = [metrics.boundingRect(line) for line in text.splitlines()]
        return (
            ceil(max(size.width() for size in sizes)),
            line_height * len(sizes),
        )

    def write_text(
        self, text, x, y, font, baseline, line_height, draw_context: QPainter, **kwargs
    ):
        metrics = QFontMetrics(font.native)
        if line_height is None:
            scaled_line_height = metrics.lineSpacing()
        else:
            scaled_line_height = line_height * font.native.pointSize()

        lines = text.splitlines()
        total_height = scaled_line_height * len(lines)

        if baseline == Baseline.TOP:
            top = y + metrics.ascent()
        elif baseline == Baseline.MIDDLE:
            top = y + metrics.ascent() - (total_height / 2)
        elif baseline == Baseline.BOTTOM:
            top = y + metrics.ascent() - total_height
        else:
            # Default to Baseline.ALPHABETIC
            top = y

        draw_context.setFont(font.native)
        for line_num, line in enumerate(lines):
            y = top + scaled_line_height * line_num
            draw_context.drawText(x, y, line)

    def get_image_data(self):
        pixmap = self.native.grab()
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        img_bytes = bytes(buffer.data())
        buffer.close()
        return img_bytes

    # Rehint
    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(size.width(), self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            max(size.height(), self.interface._MIN_HEIGHT)
        )
