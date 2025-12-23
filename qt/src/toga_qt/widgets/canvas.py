import logging
from math import ceil, cos, degrees, sin

from PySide6.QtCore import QBuffer, QIODevice, QPointF, Qt
from PySide6.QtGui import (
    QFontMetrics,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QTransform,
)
from PySide6.QtWidgets import QWidget
from travertino.size import at_least

from toga.constants import Baseline, FillRule
from toga.widgets.canvas.geometry import arc_to_bezier, sweepangle

from ..colors import native_color
from .base import Widget

logger = logging.getLogger(__name__)


class TogaCanvas(QWidget):
    def __init__(self, interface, impl):
        super().__init__()
        self.interface = interface
        self.impl = impl

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.impl.begin_path(painter)
            self.interface.context._draw(self.impl, draw_context=painter)
        except Exception:  # pragma: no cover
            logger.exception("Error rendering Canvas.")
        finally:
            # we may have saved states that need to be unwound
            # shouldn't happen normally, but can if there is an exception
            # or if there is a bug where number of saves != number of restores
            painter.end()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        button = event.button()
        match button:
            case Qt.MouseButton.LeftButton:
                self.interface.on_press(
                    int(event.position().x()), int(event.position().y())
                )
            case Qt.MouseButton.RightButton:
                self.interface.on_alt_press(
                    int(event.position().x()), int(event.position().y())
                )
            case _:  # pragma: no cover
                # Don't handle other button presses
                pass

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.interface.on_activate(
                int(event.position().x()), int(event.position().y())
            )
        else:  # pragma: no cover
            # Don't handle other button double-clicks
            pass

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        button = event.button()
        match button:
            case Qt.MouseButton.LeftButton:
                self.interface.on_release(
                    int(event.position().x()), int(event.position().y())
                )
            case Qt.MouseButton.RightButton:
                self.interface.on_alt_release(
                    int(event.position().x()), int(event.position().y())
                )
            case _:  # pragma: no cover
                # Don't handle other button releases
                pass

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # These will only fire when a mouse button is down, i.e. dragging
        button = event.button()
        match button:
            case Qt.MouseButton.LeftButton:
                self.interface.on_drag(
                    int(event.position().x()), int(event.position().y())
                )
            case Qt.MouseButton.RightButton:
                self.interface.on_alt_drag(
                    int(event.position().x()), int(event.position().y())
                )
            case _:  # pragma: no cover
                # Don't handle other mouse move events
                pass


class Canvas(Widget):
    _path: QPainterPath

    def create(self):
        self.native = TogaCanvas(self.interface, self)

    def redraw(self):
        self.native.update()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.interface.on_resize(width=width, height=height)

    # Context management
    def push_context(self, draw_context: QPainter, **kwargs):
        draw_context.save()

    def pop_context(self, draw_context: QPainter, **kwargs):
        draw_context.restore()

    # Basic paths
    def begin_path(self, draw_context: QPainter, **kwargs):
        # QPainter doesn't have the notion of a "current path" so we need to track it.
        self._path = QPainterPath()

    def close_path(self, draw_context: QPainter, **kwargs):
        self._path.closeSubpath()

    def move_to(self, x, y, draw_context: QPainter, **kwargs):
        self._path.moveTo(x, y)

    def line_to(self, x, y, draw_context, **kwargs):
        if self._path.elementCount() == 0:
            self._path.moveTo(x, y)
        else:
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
        if self._path.elementCount() == 0:
            # if this is the first point of the path, don't draw a line
            # to the start point
            self._path.moveTo(
                x + radius * cos(startangle),
                y + radius * sin(startangle),
            )

        # Qt measures angles counterclockwise from x-axis and in degrees
        self._path.arcTo(
            x - radius,
            y - radius,
            radius * 2,
            radius * 2,
            -degrees(startangle),
            -degrees(sweepangle(startangle, endangle, counterclockwise)),
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
        # Draw the ellipse unrotated and at origin
        transform = QTransform()
        transform.translate(x, y)
        transform.rotate(degrees(rotation))
        transform.scale(radiusx, radiusy)
        transform.rotate(degrees(startangle))

        # Note: we can *almost* do this using arcTo, but arcTo doesn't support rotation
        # (it must be axis-aligned), and attempts at manually rotating the points after
        # creation are awkward: easier just to use geometry routines.
        points = [
            transform.map(QPointF(x, y))
            for (x, y) in arc_to_bezier(
                sweepangle(startangle, endangle, counterclockwise)
            )
        ]

        # draw a line to the start point unless this is the first point of the path
        start = points.pop(0)
        if self._path.elementCount() == 0:
            self._path.moveTo(start)
        else:
            self._path.lineTo(start)

        for i in range(0, len(points), 3):
            cp1, cp2, end = points[i : i + 3]
            self._path.cubicTo(cp1, cp2, end)

    def rect(self, x, y, width, height, draw_context, **kwargs):
        self._path.addRect(x, y, width, height)

    # Drawing Paths

    def _get_brush(self, fill_color, **kwargs):
        return native_color(fill_color)

    def _get_pen(self, stroke_color, line_width, line_dash=None, **kwargs):
        pen = QPen()
        pen.setBrush(self._get_brush(stroke_color))
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        pen.setWidth(line_width)
        if line_dash is not None:
            pen.setDashPattern([x / line_width for x in line_dash])
        return pen

    def fill(self, color, fill_rule, draw_context: QPainter, **kwargs):
        if fill_rule == FillRule.EVENODD:
            self._path.setFillRule(Qt.FillRule.OddEvenFill)
        else:
            self._path.setFillRule(Qt.FillRule.WindingFill)
        draw_context.fillPath(self._path, self._get_brush(color))

    def stroke(self, color, line_width, line_dash, draw_context, **kwargs):
        pen = self._get_pen(color, line_width, line_dash)
        draw_context.strokePath(self._path, pen)

    # Transformations
    def rotate(self, radians, draw_context: QPainter, **kwargs):
        draw_context.rotate(degrees(radians))

    def scale(self, sx, sy, draw_context: QPainter, **kwargs):
        draw_context.scale(sx, sy)

    def translate(self, tx, ty, draw_context: QPainter, **kwargs):
        draw_context.translate(tx, ty)

    def reset_transform(self, draw_context: QPainter, **kwargs):
        draw_context.resetTransform()

    # Text
    def _line_height(self, metrics, point_size, line_height=None):
        if line_height is None:
            return metrics.lineSpacing()
        else:
            return line_height * point_size

    def _text_offsets(self, text, font, line_height):
        metrics = QFontMetrics(font.native)
        if line_height is None:
            line_height = metrics.lineSpacing()
        else:
            line_height = line_height * font.native.pointSize()

        sizes = [metrics.boundingRect(line) for line in text.splitlines()]
        if not sizes:
            return (0, 0, 0, 0, line_height)
        left_offset = ceil(min(size.x() for size in sizes))
        right_offset = ceil(max((size.width() + size.x()) for size in sizes))
        top_offset = sizes[0].y()
        return (
            left_offset,
            top_offset,
            right_offset,
            line_height * len(sizes) + top_offset,
            line_height,
        )

    def measure_text(self, text, font, line_height):
        left, top, right, bottom, _ = self._text_offsets(text, font, line_height)
        return (right - left, bottom - top)

    def write_text(
        self, text, x, y, font, baseline, line_height, draw_context: QPainter, **kwargs
    ):
        left_offset, top_offset, _, bottom_offset, scaled_line_height = (
            self._text_offsets(text, font, line_height)
        )

        lines = text.splitlines()
        total_height = bottom_offset - top_offset

        draw_context.save()
        # translate to target base point
        draw_context.translate(x, y)

        # adjust for alignment
        if baseline == Baseline.TOP:
            draw_context.translate(-left_offset, -top_offset)
        elif baseline == Baseline.MIDDLE:
            draw_context.translate(-left_offset, -top_offset - (total_height / 2))
        elif baseline == Baseline.BOTTOM:
            draw_context.translate(-left_offset, -bottom_offset)
        else:
            # Default to Baseline.ALPHABETIC
            draw_context.translate(-left_offset, 0)

        draw_context.setFont(font.native)
        path = QPainterPath()
        for line_num, line in enumerate(lines):
            y = scaled_line_height * line_num
            path.addText(0, y, font.native, line)

        if "fill_color" in kwargs:
            draw_context.fillPath(path, self._get_brush(**kwargs))
        if "stroke_color" in kwargs:
            draw_context.strokePath(path, self._get_pen(**kwargs))

        # reset state to how things were before translating
        draw_context.restore()

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
