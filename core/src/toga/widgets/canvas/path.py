# pragma: no cover
import copy
from collections.abc import Sequence
from dataclasses import dataclass
from math import pi

from toga.platform import get_platform_factory

from .drawingaction import (
    Arc,
    BezierCurveTo,
    ClosePath,
    DrawingAction,
    Ellipse,
    LineTo,
    MoveTo,
    QuadraticCurveTo,
    Rect,
)


class Path:
    def __init__(self, path: "Path | None" = None):
        if path is None:
            self.drawing_actions = []
        else:
            self.drawing_actions = copy.deepcopy(path.drawing_actions)
        self._action_target = self
        self._impl = None
        self.factory = get_platform_factory()

    @property
    def impl(self):
        if self._impl is None:
            self._impl = self.compile()
        return self._impl

    def add_path(self, path: "Path", transform: Sequence[float] | None = None):
        """Adds another path to the current path with an optional transform.

        :param path: The Path being added.
        :param transform: The Transform to apply to the added path.
        :returns: The `AddPath` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        add_path = AddPath(path, transform)
        self._action_target.drawing_actions.append(add_path)
        self._redraw_with_warning_if_state()
        return add_path

    def close_path(self):
        """Close the current path in the canvas state.

        This closes the current subpath by drawing a line from the current point
        to the starting point of the current subpath.

        :returns: The `ClosePath`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction] for the operation.
        """
        close_path = ClosePath()
        self._action_target.drawing_actions.append(close_path)
        self._redraw_with_warning_if_state()
        return close_path

    def move_to(self, x: float, y: float) -> MoveTo:
        """Moves the current point without drawing.

        :param x: The x coordinate of the new current point.
        :param y: The y coordinate of the new current point.
        :returns: The `MoveTo` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        move_to = MoveTo(x, y)
        self._action_target.drawing_actions.append(move_to)
        self._redraw_with_warning_if_state()
        return move_to

    def line_to(self, x: float, y: float) -> LineTo:
        """Draw a line segment ending at a point.

        :param x: The x coordinate for the end point of the line segment.
        :param y: The y coordinate for the end point of the line segment.
        :returns: The `LineTo` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        line_to = LineTo(x, y)
        self._action_target.drawing_actions.append(line_to)
        self._redraw_with_warning_if_state()
        return line_to

    def bezier_curve_to(
        self,
        cp1x: float,
        cp1y: float,
        cp2x: float,
        cp2y: float,
        x: float,
        y: float,
    ) -> BezierCurveTo:
        """Draw a Bézier curve.

        A Bézier curve requires three points. The first two are control points; the
        third is the end point for the curve. The starting point is the last point in
        the current path, which can be changed using `move_to()` before creating the
        Bézier curve.

        :param cp1y: The y coordinate for the first control point of the Bézier curve.
        :param cp1x: The x coordinate for the first control point of the Bézier curve.
        :param cp2x: The x coordinate for the second control point of the Bézier curve.
        :param cp2y: The y coordinate for the second control point of the Bézier curve.
        :param x: The x coordinate for the end point.
        :param y: The y coordinate for the end point.
        :returns: The `BezierCurveTo`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction] for the operation.
        """
        bezier_curve_to = BezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)
        self._action_target.drawing_actions.append(bezier_curve_to)
        self._redraw_with_warning_if_state()
        return bezier_curve_to

    def quadratic_curve_to(
        self,
        cpx: float,
        cpy: float,
        x: float,
        y: float,
    ) -> QuadraticCurveTo:
        """Draw a quadratic curve.

        A quadratic curve requires two points. The first point is a control point; the
        second is the end point. The starting point of the curve is the last point in
        the current path, which can be changed using `moveTo()` before creating the
        quadratic curve.

        :param cpx: The x axis of the coordinate for the control point of the quadratic
            curve.
        :param cpy: The y axis of the coordinate for the control point of the quadratic
            curve.
        :param x: The x axis of the coordinate for the end point.
        :param y: The y axis of the coordinate for the end point.
        :returns: The `QuadraticCurveTo`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction] for the operation.
        """
        quadratic_curve_to = QuadraticCurveTo(cpx, cpy, x, y)
        self._action_target.drawing_actions.append(quadratic_curve_to)
        self._redraw_with_warning_if_state()
        return quadratic_curve_to

    def arc(
        self,
        x: float,
        y: float,
        radius: float,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        counterclockwise: bool | None = None,
        anticlockwise: bool | None = None,  # DEPRECATED
    ) -> Arc:
        """Draw a circular arc.

        A full circle will be drawn by default; an arc can be drawn by specifying a
        start and end angle.

        :param x: The X coordinate of the circle's center.
        :param y: The Y coordinate of the circle's center.
        :param startangle: The start angle in radians, measured clockwise from the
            positive X axis.
        :param endangle: The end angle in radians, measured clockwise from the positive
            X axis.
        :param counterclockwise: If true, the arc is swept counterclockwise. The default
            is clockwise.
        :param anticlockwise: **DEPRECATED** - Use `counterclockwise`.
        :returns: The `Arc` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        arc = Arc(x, y, radius, startangle, endangle, counterclockwise, anticlockwise)
        self._action_target.drawing_actions.append(arc)
        self._redraw_with_warning_if_state()
        return arc

    def ellipse(
        self,
        x: float,
        y: float,
        radiusx: float,
        radiusy: float,
        rotation: float = 0.0,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        counterclockwise: bool | None = None,
        anticlockwise: bool | None = None,  # DEPRECATED
    ) -> Ellipse:
        """Draw an elliptical arc.

        A full ellipse will be drawn by default; an arc can be drawn by specifying a
        start and end angle.

        :param x: The X coordinate of the ellipse's center.
        :param y: The Y coordinate of the ellipse's center.
        :param radiusx: The ellipse's horizontal axis radius.
        :param radiusy: The ellipse's vertical axis radius.
        :param rotation: The ellipse's rotation in radians, measured clockwise around
            its center.
        :param startangle: The start angle in radians, measured clockwise from the
            positive X axis.
        :param endangle: The end angle in radians, measured clockwise from the positive
            X axis.
        :param counterclockwise: If true, the arc is swept counterclockwise. The default
            is clockwise.
        :param anticlockwise: **DEPRECATED** - Use `counterclockwise`.
        :returns: The `Ellipse` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        ellipse = Ellipse(
            x,
            y,
            radiusx,
            radiusy,
            rotation,
            startangle,
            endangle,
            counterclockwise,
            anticlockwise,
        )
        self._action_target.drawing_actions.append(ellipse)
        self._redraw_with_warning_if_state()
        return ellipse

    def rect(self, x: float, y: float, width: float, height: float) -> Rect:
        """Draw a rectangle.

        :param x: The horizontal coordinate of the left of the rectangle.
        :param y: The vertical coordinate of the top of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :returns: The `Rect` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """

        rect = Rect(x, y, width, height)
        self._action_target.drawing_actions.append(rect)
        self._redraw_with_warning_if_state()
        return rect

    def _redraw_with_warning_if_state(self):
        pass

    def compile(self):
        print("compiling")
        impl = self.factory.Path()
        for action in self.drawing_actions:
            print(action)
            action._draw(impl)
        return impl


@dataclass(repr=False)
class AddPath(DrawingAction):
    path: Path
    transform: Sequence[float] | None = None

    def _draw(self, context):
        context.add_path(self.path.impl, self.transform)
