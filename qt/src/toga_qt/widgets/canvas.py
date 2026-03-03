import logging
from math import ceil, cos, degrees, sin

from PySide6.QtCore import QBuffer, QIODevice, QPointF, QRectF, Qt
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

from toga.colors import rgb
from toga.constants import Baseline, FillRule
from toga.widgets.canvas.geometry import arc_to_bezier, round_rect, sweepangle

from ..colors import native_color
from .base import Widget

logger = logging.getLogger(__name__)


BLACK = native_color(rgb(0, 0, 0))


class State:
    """Track transform and fill/stroke-related properties."""

    def __init__(self, former_state=None):
        self.transform = QTransform()
        if former_state:
            self.fill_style = former_state.fill_style
            self.stroke = QPen(former_state.stroke)
        else:
            self.fill_style = BLACK
            self.stroke = QPen(BLACK)
            self.stroke.setCapStyle(Qt.PenCapStyle.FlatCap)
            self.stroke.setWidth(2.0)
            self.stroke.setJoinStyle(Qt.MiterJoin)
            # Qt measures miter length along the edge of the stroke, from where the
            # bevel would end to the point.
            self.stroke.setMiterLimit(4.899)  # sqrt(24)


class Context:
    _path: QPainterPath

    def __init__(self, impl, native):
        self.impl = impl
        self.native = native
        self.states = [State()]

        # Backwards compatibility for Toga <= 0.5.3
        self.in_fill = False
        self.in_stroke = False

    @property
    def state(self):
        return self.states[-1]

    # Context management
    def save(self):
        self.states.append(State(self.state))
        self.native.save()

    def restore(self):
        # Transform active path to current coordinates
        self._path = self.state.transform.map(self._path)
        self.states.pop()
        self.native.restore()

    # Setting attributes
    def set_fill_style(self, color):
        self.state.fill_style = native_color(color)

    def set_line_dash(self, line_dash):
        self.state.stroke.setDashPattern(
            [x / self.state.stroke.width() for x in line_dash]
        )

    def set_line_width(self, line_width):
        self.state.stroke.setWidth(line_width)

    def set_stroke_style(self, color):
        self.state.stroke.setColor(native_color(color))

    # Basic paths
    def begin_path(self):
        # QPainter doesn't have the notion of a "current path" so we need to track it.
        self._path = QPainterPath()

    def close_path(self):
        self._path.closeSubpath()

    def move_to(self, x, y):
        self._path.moveTo(x, y)

    def line_to(self, x, y):
        if self._path.elementCount() == 0:
            self._path.moveTo(x, y)
        else:
            self._path.lineTo(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self._path.cubicTo(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self._path.quadTo(cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, counterclockwise):
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

    def rect(self, x, y, width, height):
        self._path.addRect(x, y, width, height)

    def round_rect(self, x, y, width, height, radii):
        round_rect(self, x, y, width, height, radii)

    # Drawing Paths

    def fill(self, fill_rule):
        if fill_rule == FillRule.EVENODD:
            self._path.setFillRule(Qt.FillRule.OddEvenFill)
        else:
            self._path.setFillRule(Qt.FillRule.WindingFill)
        self.native.fillPath(self._path, self.state.fill_style)

    def stroke(self):
        self.native.strokePath(self._path, self.state.stroke)

    # Transformations
    def rotate(self, radians):
        self.native.rotate(degrees(radians))

        # Update state transform
        self.state.transform.rotateRadians(radians)

        # Transform active path to current coordinates
        inverse = QTransform()
        inverse.rotateRadians(-radians)
        self._path = inverse.map(self._path)

    def scale(self, sx, sy):
        # Can't apply inverse transform if scale is 0,
        # so use a small epsilon which will almost be the same
        if sx == 0:
            sx = 2**-24
        if sy == 0:
            sy = 2**-24

        self.native.scale(sx, sy)

        # Update state transform
        self.state.transform.scale(sx, sy)

        # Transform active path to current coordinates
        inverse = QTransform()
        inverse.scale(1 / sx, 1 / sy)
        self._path = inverse.map(self._path)

    def translate(self, tx, ty):
        self.native.translate(tx, ty)

        # Update state transform
        self.state.transform.translate(tx, ty)

        # Transform active path to current coordinates
        inverse = QTransform()
        inverse.translate(-tx, -ty)
        self._path = inverse.map(self._path)

    def reset_transform(self):
        transform = self.native.transform()
        self.native.resetTransform()

        # Update state transform
        inverse, _ = transform.inverted()
        self._path = transform.map(self._path)
        self.state.transform *= inverse

    # Text
    def write_text(self, text, x, y, font, baseline, line_height):
        left_offset, top_offset, _, bottom_offset, scaled_line_height = (
            self.impl._text_offsets(text, font, line_height)
        )

        lines = text.splitlines()
        total_height = bottom_offset - top_offset

        self.save()
        # translate to target base point
        self.translate(x, y)

        # adjust for alignment
        if baseline == Baseline.TOP:
            self.translate(-left_offset, -top_offset)
        elif baseline == Baseline.MIDDLE:
            self.translate(-left_offset, -top_offset - (total_height / 2))
        elif baseline == Baseline.BOTTOM:
            self.translate(-left_offset, -bottom_offset)
        else:
            # Default to Baseline.ALPHABETIC
            self.translate(-left_offset, 0)

        self.native.setFont(font.native)
        path = QPainterPath()
        for line_num, line in enumerate(lines):
            y = scaled_line_height * line_num
            path.addText(0, y, font.native, line)

        if self.in_fill:
            self.native.fillPath(path, self.state.fill_style)
        if self.in_stroke:
            self.native.strokePath(path, self.state.stroke)

        # reset state to how things were before translating
        self.restore()

    # Bitmap images
    def draw_image(self, image, x, y, width, height):
        self.native.drawImage(QRectF(x, y, width, height), image._impl.native)


class TogaCanvas(QWidget):
    def __init__(self, interface, impl):
        super().__init__()
        self.interface = interface
        self.impl = impl

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        context = Context(self.impl, painter)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            context.begin_path()
            self.interface.root_state._draw(context)
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
    def create(self):
        self.native = TogaCanvas(self.interface, self)

    def redraw(self):
        self.native.update()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.interface.on_resize(width=width, height=height)

    # Text
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
