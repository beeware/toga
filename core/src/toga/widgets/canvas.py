from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from contextlib import contextmanager
from math import cos, pi, sin, tan
from typing import TYPE_CHECKING, Protocol

from travertino.colors import Color

import toga
from toga.colors import BLACK, color as parse_color
from toga.constants import Baseline, FillRule
from toga.fonts import SYSTEM, SYSTEM_DEFAULT_FONT_SIZE, Font
from toga.handlers import wrapped_handler

from .base import Widget

if TYPE_CHECKING:
    from toga.images import ImageT

#######################################################################################
# Simple drawing objects
#######################################################################################


class DrawingObject(ABC):
    """A drawing operation in a :any:`Context`.

    Every context drawing method creates a ``DrawingObject``, adds it to the context,
    and returns it. Each argument passed to the method becomes a property of the
    ``DrawingObject``, which can be modified as shown in the `Usage`_ section.

    ``DrawingObjects`` can also be created manually, then added to a context using the
    :meth:`~Context.append` or :meth:`~Context.insert` methods. Their constructors take
    the same arguments as the corresponding :any:`Context` method, and their classes
    have the same names, but capitalized:

    * :meth:`toga.widgets.canvas.Arc <Context.arc>`
    * :meth:`toga.widgets.canvas.BeginPath <Context.begin_path>`
    * :meth:`toga.widgets.canvas.BezierCurveTo <Context.bezier_curve_to>`
    * :meth:`toga.widgets.canvas.ClosePath <Context.close_path>`
    * :meth:`toga.widgets.canvas.Ellipse <Context.ellipse>`
    * :meth:`toga.widgets.canvas.Fill <Context.fill>`
    * :meth:`toga.widgets.canvas.LineTo <Context.line_to>`
    * :meth:`toga.widgets.canvas.MoveTo <Context.move_to>`
    * :meth:`toga.widgets.canvas.QuadraticCurveTo <Context.quadratic_curve_to>`
    * :meth:`toga.widgets.canvas.Rect <Context.rect>`
    * :meth:`toga.widgets.canvas.ResetTransform <Context.reset_transform>`
    * :meth:`toga.widgets.canvas.Rotate <Context.rotate>`
    * :meth:`toga.widgets.canvas.Scale <Context.scale>`
    * :meth:`toga.widgets.canvas.Stroke <Context.stroke>`
    * :meth:`toga.widgets.canvas.Translate <Context.translate>`
    * :meth:`toga.widgets.canvas.WriteText <Context.write_text>`
    """

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def _draw(self, impl, **kwargs): ...


class BeginPath(DrawingObject):
    def _draw(self, impl, **kwargs):
        impl.begin_path(**kwargs)


class ClosePath(DrawingObject):
    def _draw(self, impl, **kwargs):
        impl.close_path(**kwargs)


class Fill(DrawingObject):
    def __init__(
        self,
        color: str = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
    ):
        super().__init__()
        self.color = color
        self.fill_rule = fill_rule

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(color={self.color!r}, "
            f"fill_rule={self.fill_rule})"
        )

    def _draw(self, impl, **kwargs):
        impl.fill(self.color, self.fill_rule, **kwargs)

    @property
    def fill_rule(self) -> FillRule:
        return self._fill_rule

    @fill_rule.setter
    def fill_rule(self, fill_rule: FillRule):
        self._fill_rule = fill_rule

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color | str | None):
        if value is None:
            self._color = parse_color(BLACK)
        else:
            self._color = parse_color(value)

    ###########################################################################
    # 2023-07 Backwards incompatibility
    ###########################################################################

    # `context.fill()` used to be a context manager, but is now a primitive.
    # If you try to use the Fill drawing object as a context, raise an exception.
    def __enter__(self):
        raise RuntimeError("Context.fill() has been renamed Context.Fill().")

    def __exit__(self):  # pragma: no cover
        # This method is required to make the object a context manager, but as the
        # __enter__ method raises an exception, the __exit__ can't be called.
        pass


class Stroke(DrawingObject):
    def __init__(
        self,
        color: Color | str | None = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        super().__init__()
        self.color = color
        self.line_width = line_width
        self.line_dash = line_dash

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(color={self.color!r}, "
            f"line_width={self.line_width}, line_dash={self.line_dash!r})"
        )

    def _draw(self, impl, **kwargs):
        impl.stroke(self.color, self.line_width, self.line_dash, **kwargs)

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color | str | None):
        if value is None:
            self._color = parse_color(BLACK)
        else:
            self._color = parse_color(value)

    @property
    def line_width(self) -> float:
        return self._line_width

    @line_width.setter
    def line_width(self, value: float):
        self._line_width = float(value)

    @property
    def line_dash(self) -> list[float] | None:
        return self._line_dash

    @line_dash.setter
    def line_dash(self, value: list[float] | None):
        self._line_dash = value

    ###########################################################################
    # 2023-07 Backwards incompatibility
    ###########################################################################

    # `context.stroke()` used to be a context managger, but is now a primitive.
    # If you try to use the Stroke drawing object as a context, raise an exception.
    def __enter__(self):
        raise RuntimeError("Context.stroke() has been renamed Context.Stroke().")

    def __exit__(self):  # pragma: no cover
        # This method is required to make the object a context manager, but as the
        # __enter__ method raises an exception, the __exit__ can't be called.
        pass


class MoveTo(DrawingObject):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl, **kwargs):
        impl.move_to(self.x, self.y, **kwargs)


class LineTo(DrawingObject):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl, **kwargs):
        impl.line_to(self.x, self.y, **kwargs)


class BezierCurveTo(DrawingObject):
    def __init__(
        self, cp1x: float, cp1y: float, cp2x: float, cp2y: float, x: float, y: float
    ):
        self.cp1x = cp1x
        self.cp1y = cp1y
        self.cp2x = cp2x
        self.cp2y = cp2y
        self.x = x
        self.y = y

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(cp1x={self.cp1x}, cp1y={self.cp1y}, "
            f"cp2x={self.cp2x}, cp2y={self.cp2y}, "
            f"x={self.x}, y={self.y})"
        )

    def _draw(self, impl, **kwargs):
        impl.bezier_curve_to(
            self.cp1x, self.cp1y, self.cp2x, self.cp2y, self.x, self.y, **kwargs
        )


class QuadraticCurveTo(DrawingObject):
    def __init__(self, cpx: float, cpy: float, x: float, y: float):
        self.cpx = cpx
        self.cpy = cpy
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(cpx={self.cpx}, cpy={self.cpy}, x={self.x}, y={self.y})"

    def _draw(self, impl, **kwargs):
        impl.quadratic_curve_to(self.cpx, self.cpy, self.x, self.y, **kwargs)


class Arc(DrawingObject):
    def __init__(
        self,
        x: float,
        y: float,
        radius: float,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        anticlockwise: bool = False,
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"radius={self.radius}, startangle={self.startangle:.3f}, "
            f"endangle={self.endangle:.3f}, anticlockwise={self.anticlockwise})"
        )

    def _draw(self, impl, **kwargs):
        impl.arc(
            self.x,
            self.y,
            self.radius,
            self.startangle,
            self.endangle,
            self.anticlockwise,
            **kwargs,
        )


class Ellipse(DrawingObject):
    def __init__(
        self,
        x: float,
        y: float,
        radiusx: float,
        radiusy: float,
        rotation: float = 0.0,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        anticlockwise: bool = False,
    ):
        self.x = x
        self.y = y
        self.radiusx = radiusx
        self.radiusy = radiusy
        self.rotation = rotation
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"radiusx={self.radiusx}, radiusy={self.radiusy}, "
            f"rotation={self.rotation:.3f}, startangle={self.startangle:.3f}, "
            f"endangle={self.endangle:.3f}, anticlockwise={self.anticlockwise})"
        )

    def _draw(self, impl, **kwargs):
        impl.ellipse(
            self.x,
            self.y,
            self.radiusx,
            self.radiusy,
            self.rotation,
            self.startangle,
            self.endangle,
            self.anticlockwise,
            **kwargs,
        )


class Rect(DrawingObject):
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"width={self.width}, height={self.height})"
        )

    def _draw(self, impl, **kwargs):
        impl.rect(self.x, self.y, self.width, self.height, **kwargs)


class WriteText(DrawingObject):
    def __init__(
        self,
        text: str,
        x: float = 0.0,
        y: float = 0.0,
        font: Font | None = None,
        baseline: Baseline = Baseline.ALPHABETIC,
    ):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.baseline = baseline

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(text={self.text!r}, x={self.x}, y={self.y}, "
            f"font={self.font!r}, baseline={self.baseline})"
        )

    def _draw(self, impl, **kwargs):
        impl.write_text(
            str(self.text), self.x, self.y, self.font._impl, self.baseline, **kwargs
        )

    @property
    def font(self) -> Font:
        return self._font

    @font.setter
    def font(self, value: Font | None):
        if value is None:
            self._font = Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE)
        else:
            self._font = value


class Rotate(DrawingObject):
    def __init__(self, radians: float):
        self.radians = radians

    def __repr__(self):
        return f"{self.__class__.__name__}(radians={self.radians:.3f})"

    def _draw(self, impl, **kwargs):
        impl.rotate(self.radians, **kwargs)


class Scale(DrawingObject):
    def __init__(self, sx: float, sy: float):
        self.sx = sx
        self.sy = sy

    def __repr__(self):
        return f"{self.__class__.__name__}(sx={self.sx:.3f}, sy={self.sy:.3f})"

    def _draw(self, impl, **kwargs):
        impl.scale(self.sx, self.sy, **kwargs)


class Translate(DrawingObject):
    def __init__(self, tx: float, ty: float):
        self.tx = tx
        self.ty = ty

    def __repr__(self):
        return f"{self.__class__.__name__}(tx={self.tx}, ty={self.ty})"

    def _draw(self, impl, **kwargs):
        impl.translate(self.tx, self.ty, **kwargs)


class ResetTransform(DrawingObject):
    def _draw(self, impl, **kwargs):
        impl.reset_transform(**kwargs)


#######################################################################################
# Drawing Contexts
#######################################################################################


class Context(DrawingObject):
    """A drawing context for a canvas.

    You should not create a :class:`~toga.widgets.canvas.Context` directly; instead,
    you should use the :meth:`~Context.Context` method on an existing context,
    or use :any:`Canvas.context` to access the root context of the canvas.
    """

    def __init__(self, canvas: toga.Canvas, **kwargs):
        # kwargs used to support multiple inheritance
        super().__init__(**kwargs)
        self._canvas = canvas
        self.drawing_objects = []

    def _draw(self, impl, **kwargs):
        impl.push_context(**kwargs)
        for obj in self.drawing_objects:
            obj._draw(impl, **kwargs)
        impl.pop_context(**kwargs)

    ###########################################################################
    # Methods to keep track of the canvas, automatically redraw it
    ###########################################################################

    @property
    def canvas(self) -> Canvas:
        """The canvas that is associated with this drawing context."""
        return self._canvas

    def redraw(self):
        """Calls :any:`Canvas.redraw` on the parent Canvas."""
        self.canvas.redraw()

    ###########################################################################
    # Operations on drawing objects
    ###########################################################################

    def __len__(self) -> int:
        """Returns the number of drawing objects that are in this context."""
        return len(self.drawing_objects)

    def __getitem__(self, index: int) -> DrawingObject:
        """Returns the drawing object at the given index."""
        return self.drawing_objects[index]

    def append(self, obj: DrawingObject):
        """Append a drawing object to the context.

        :param obj: The drawing object to add to the context.
        """
        self.drawing_objects.append(obj)
        self.redraw()

    def insert(self, index: int, obj: DrawingObject):
        """Insert a drawing object into the context at a specific index.

        :param index: The index at which the drawing object should be inserted.
        :param obj: The drawing object to add to the context.
        """
        self.drawing_objects.insert(index, obj)
        self.redraw()

    def remove(self, obj: DrawingObject):
        """Remove a drawing object from the context.

        :param obj: The drawing object to remove.
        """
        self.drawing_objects.remove(obj)
        self.redraw()

    def clear(self):
        """Remove all drawing objects from the context."""
        self.drawing_objects.clear()
        self.redraw()

    ###########################################################################
    # Path manipulation
    ###########################################################################

    def begin_path(self):
        """Start a new path in the canvas context.

        :returns: The ``BeginPath`` :any:`DrawingObject` for the operation.
        """
        begin_path = BeginPath()
        self.append(begin_path)
        return begin_path

    def close_path(self):
        """Close the current path in the canvas context.

        This closes the current path as a simple drawing operation. It should be paired
        with a :meth:`~toga.widgets.canvas.Context.begin_path()` operation; or, to
        complete a complete closed path, use the
        :meth:`~toga.widgets.canvas.Context.ClosedPath()` context manager.

        :returns: The ``ClosePath`` :any:`DrawingObject` for the operation.
        """
        close_path = ClosePath()
        self.append(close_path)
        return close_path

    def move_to(self, x: float, y: float):
        """Moves the current point of the canvas context without drawing.

        :param x: The x coordinate of the new current point.
        :param y: The y coordinate of the new current point.
        :returns: The ``MoveTo`` :any:`DrawingObject` for the operation.
        """
        move_to = MoveTo(x, y)
        self.append(move_to)
        return move_to

    def line_to(self, x: float, y: float):
        """Draw a line segment ending at a point in the canvas context.

        :param x: The x coordinate for the end point of the line segment.
        :param y: The y coordinate for the end point of the line segment.
        :returns: The ``LineTo`` :any:`DrawingObject` for the operation.
        """
        line_to = LineTo(x, y)
        self.append(line_to)
        return line_to

    def bezier_curve_to(
        self,
        cp1x: float,
        cp1y: float,
        cp2x: float,
        cp2y: float,
        x: float,
        y: float,
    ):
        """Draw a Bézier curve in the canvas context.

        A Bézier curve requires three points. The first two are control points; the
        third is the end point for the curve. The starting point is the last point in
        the current path, which can be changed using move_to() before creating the
        Bézier curve.

        :param cp1y: The y coordinate for the first control point of the Bézier curve.
        :param cp1x: The x coordinate for the first control point of the Bézier curve.
        :param cp2x: The x coordinate for the second control point of the Bézier curve.
        :param cp2y: The y coordinate for the second control point of the Bézier curve.
        :param x: The x coordinate for the end point.
        :param y: The y coordinate for the end point.
        :returns: The ``BezierCurveTo`` :any:`DrawingObject` for the operation.
        """
        bezier_curve_to = BezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)
        self.append(bezier_curve_to)
        return bezier_curve_to

    def quadratic_curve_to(self, cpx: float, cpy: float, x: float, y: float):
        """Draw a quadratic curve in the canvas context.

        A quadratic curve requires two points. The first point is a control point; the
        second is the end point. The starting point of the curve is the last point in
        the current path, which can be changed using ``moveTo()`` before creating the
        quadratic curve.

        :param cpx: The x axis of the coordinate for the control point of the quadratic
            curve.
        :param cpy: The y axis of the coordinate for the control point of the quadratic
            curve.
        :param x: The x axis of the coordinate for the end point.
        :param y: The y axis of the coordinate for the end point.
        :returns: The ``QuadraticCurveTo`` :any:`DrawingObject` for the operation.
        """
        quadratic_curve_to = QuadraticCurveTo(cpx, cpy, x, y)
        self.append(quadratic_curve_to)
        return quadratic_curve_to

    def arc(
        self,
        x: float,
        y: float,
        radius: float,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        anticlockwise: bool = False,
    ):
        """Draw a circular arc in the canvas context.

        A full circle will be drawn by default; an arc can be drawn by specifying a
        start and end angle.

        :param x: The X coordinate of the circle's center.
        :param y: The Y coordinate of the circle's center.
        :param startangle: The start angle in radians, measured clockwise from the
            positive X axis.
        :param endangle: The end angle in radians, measured clockwise from the positive
            X axis.
        :param anticlockwise: If true, the arc is swept anticlockwise. The default is
            clockwise.
        :returns: The ``Arc`` :any:`DrawingObject` for the operation.
        """
        arc = Arc(x, y, radius, startangle, endangle, anticlockwise)
        self.append(arc)
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
        anticlockwise: bool = False,
    ):
        """Draw an elliptical arc in the canvas context.

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
        :param anticlockwise: If true, the arc is swept anticlockwise. The default is
            clockwise.
        :returns: The ``Ellipse`` :any:`DrawingObject` for the operation.
        """
        ellipse = Ellipse(
            x,
            y,
            radiusx,
            radiusy,
            rotation,
            startangle,
            endangle,
            anticlockwise,
        )
        self.append(ellipse)
        return ellipse

    def rect(self, x: float, y: float, width: float, height: float):
        """Draw a rectangle in the canvas context.

        :param x: The horizontal coordinate of the left of the rectangle.
        :param y: The vertical coordinate of the top of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :returns: The ``Rect`` :any:`DrawingObject` for the operation.
        """
        rect = Rect(x, y, width, height)
        self.append(rect)
        return rect

    def fill(
        self,
        color: str = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
        preserve=None,  # DEPRECATED
    ):
        """Fill the current path.

        The fill can use either the `Non-Zero
        <https://en.wikipedia.org/wiki/Nonzero-rule>`__ or `Even-Odd
        <https://en.wikipedia.org/wiki/Even-odd_rule>`__ winding rule for filling paths.

        :param fill_rule: `nonzero` is the non-zero winding rule; `evenodd` is the
            even-odd winding rule.
        :param color: The fill color.
        :param preserve: **DEPRECATED**: this argument has no effect.
        :returns: The ``Fill`` :any:`DrawingObject` for the operation.
        """
        if preserve is not None:
            warnings.warn(
                "The `preserve` argument on fill() has been deprecated.",
                DeprecationWarning,
            )

        fill = Fill(color, fill_rule)
        self.append(fill)
        return fill

    def stroke(
        self,
        color: str = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        """Draw the current path as a stroke.

        :param color: The color for the stroke.
        :param line_width: The width of the stroke.
        :param line_dash: The dash pattern to follow when drawing the line, expressed as
            alternating lengths of dashes and spaces. The default is a solid line.
        :returns: The ``Stroke`` :any:`DrawingObject` for the operation.
        """
        stroke = Stroke(color, line_width, line_dash)
        self.append(stroke)
        return stroke

    ###########################################################################
    # Text drawing
    ###########################################################################

    def write_text(
        self,
        text: str,
        x: float = 0.0,
        y: float = 0.0,
        font: Font | None = None,
        baseline: Baseline = Baseline.ALPHABETIC,
    ):
        """Write text at a given position in the canvas context.

        Drawing text is effectively a series of path operations, so the text will have
        the color and fill properties of the canvas context.

        :param text: The text to draw. Newlines will cause line breaks, but long lines
            will not be wrapped.
        :param x: The X coordinate of the text's left edge.
        :param y: The Y coordinate: its meaning depends on ``baseline``.
        :param font: The font in which to draw the text. The default is the system font.
        :param baseline: Alignment of text relative to the Y coordinate.
        :returns: The ``WriteText`` :any:`DrawingObject` for the operation.
        """
        write_text = WriteText(text, x, y, font, baseline)
        self.append(write_text)
        return write_text

    ###########################################################################
    # Transformations
    ###########################################################################
    def rotate(self, radians: float):
        """Add a rotation to the canvas context.

        :param radians: The angle to rotate clockwise in radians.
        :returns: The ``Rotate`` :any:`DrawingObject` for the transformation.
        """
        rotate = Rotate(radians)
        self.append(rotate)
        return rotate

    def scale(self, sx: float, sy: float):
        """Add a scaling transformation to the canvas context.

        :param sx: Scale factor for the X dimension. A negative value flips the
            image horizontally.
        :param sy: Scale factor for the Y dimension. A negative value flips the
            image vertically.
        :returns: The ``Scale`` :any:`DrawingObject` for the transformation.
        """
        scale = Scale(sx, sy)
        self.append(scale)
        return scale

    def translate(self, tx: float, ty: float):
        """Add a translation to the canvas context.

        :param tx: Translation for the X dimension.
        :param ty: Translation for the Y dimension.
        :returns: The ``Translate`` :any:`DrawingObject` for the transformation.
        """
        translate = Translate(tx, ty)
        self.append(translate)
        return translate

    def reset_transform(self):
        """Reset all transformations in the canvas context.

        :returns: A ``ResetTransform`` :any:`DrawingObject`.
        """
        reset_transform = ResetTransform()
        self.append(reset_transform)
        return reset_transform

    ###########################################################################
    # Subcontexts of this context
    ###########################################################################

    @contextmanager
    def Context(self):
        """Construct and yield a new sub-:class:`~toga.widgets.canvas.Context` within
        this context.

        :yields: The new :class:`~toga.widgets.canvas.Context` object.
        """
        context = Context(canvas=self._canvas)
        self.append(context)
        yield context
        self.redraw()

    @contextmanager
    def ClosedPath(self, x: float | None = None, y: float | None = None):
        """Construct and yield a new :class:`~toga.widgets.canvas.ClosedPath`
        sub-context that will draw a closed path, starting from an origin.

        This is a context manager; it creates a new path and moves to the start
        coordinate; when the context exits, the path is closed. For fine-grained control
        of a path, you can use :meth:`~toga.widgets.canvas.Context.begin_path` and
        :meth:`~toga.widgets.canvas.Context.close_path`.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :yields: The :class:`~toga.widgets.canvas.ClosedPathContext` context object.
        """
        closed_path = ClosedPathContext(canvas=self.canvas, x=x, y=y)
        self.append(closed_path)
        yield closed_path

    @contextmanager
    def Fill(
        self,
        x: float | None = None,
        y: float | None = None,
        color: str = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
    ):
        """Construct and yield a new :class:`~toga.widgets.canvas.Fill` sub-context
        within this context.

        This is a context manager; it creates a new path, and moves to the start
        coordinate; when the context exits, the path is closed with a fill. For
        fine-grained control of a path, you can use
        :class:`~toga.widgets.canvas.Context.begin_path`,
        :class:`~toga.widgets.canvas.Context.move_to`,
        :class:`~toga.widgets.canvas.Context.close_path` and
        :class:`~toga.widgets.canvas.Context.fill`.

        If both an x and y coordinate is provided, the drawing context will begin with
        a ``move_to`` operation in that context.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :param fill_rule: `nonzero` is the non-zero winding rule; `evenodd` is the
            even-odd winding rule.
        :param color: The fill color.
        :yields: The new :class:`~toga.widgets.canvas.FillContext` context object.
        """
        fill = FillContext(
            canvas=self.canvas,
            x=x,
            y=y,
            color=color,
            fill_rule=fill_rule,
        )
        self.append(fill)
        yield fill

    @contextmanager
    def Stroke(
        self,
        x: float | None = None,
        y: float | None = None,
        color: str = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        """Construct and yield a new :class:`~toga.widgets.canvas.Stroke` sub-context
        within this context.

        This is a context manager; it creates a new path, and moves to the start
        coordinate; when the context exits, the path is closed with a stroke. For
        fine-grained control of a path, you can use
        :class:`~toga.widgets.canvas.Context.begin_path`,
        :class:`~toga.widgets.canvas.Context.move_to`,
        :class:`~toga.widgets.canvas.Context.close_path` and
        :class:`~toga.widgets.canvas.Context.stroke`.

        If both an x and y coordinate is provided, the drawing context will begin with
        a ``move_to`` operation in that context.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :param color: The color for the stroke.
        :param line_width: The width of the stroke.
        :param line_dash: The dash pattern to follow when drawing the line. Default is a
            solid line.
        :yields: The new :class:`~toga.widgets.canvas.StrokeContext` context object.
        """
        stroke = StrokeContext(
            canvas=self.canvas,
            x=x,
            y=y,
            color=color,
            line_width=line_width,
            line_dash=line_dash,
        )
        self.append(stroke)
        yield stroke

    ###########################################################################
    # 2023-07 Backwards incompatibility
    ###########################################################################

    def new_path(self):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.begin_path`."""
        warnings.warn(
            "Context.new_path() has been renamed Context.begin_path()",
            DeprecationWarning,
        )
        return self.begin_path()

    def context(self):
        """**DEPRECATED** - use :meth:`~toga.widgets.canvas.Context.Context`"""
        warnings.warn(
            "Context.context() has been renamed Context.Context()", DeprecationWarning
        )
        return self.Context()

    def closed_path(self, x: float, y: float):
        """**DEPRECATED** - use :meth:`~toga.widgets.canvas.Context.ClosedPath`"""
        warnings.warn(
            "Context.closed_path() has been renamed Context.ClosedPath()",
            DeprecationWarning,
        )
        return self.ClosedPath(x, y)


class ClosedPathContext(Context):
    """A drawing context that will build a closed path, starting from an
    origin.

    This is a context manager; it creates a new path and moves to the start coordinate;
    when the context exits, the path is closed. For fine-grained control of a path, you
    can use :class:`~toga.widgets.canvas.Context.begin_path`,
    :class:`~toga.widgets.canvas.Context.move_to` and
    :class:`~toga.widgets.canvas.Context.close_path`.

    If both an x and y coordinate is provided, the drawing context will begin with
    a ``move_to`` operation in that context.

    You should not create a :class:`~toga.widgets.canvas.ClosedPathContext` context
    directly; instead, you should use the
    :meth:`~toga.widgets.canvas.Context.ClosedPath` method on an existing context.
    """

    def __init__(
        self,
        canvas: toga.Canvas,
        x: float | None = None,
        y: float | None = None,
    ):
        super().__init__(canvas=canvas)
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl, **kwargs):
        """Used by parent to draw all objects that are part of the context."""
        impl.push_context(**kwargs)
        impl.begin_path(**kwargs)
        if self.x is not None and self.y is not None:
            impl.move_to(x=self.x, y=self.y, **kwargs)

        sub_kwargs = kwargs.copy()
        for obj in self.drawing_objects:
            obj._draw(impl, **sub_kwargs)

        impl.close_path(**kwargs)
        impl.pop_context(**kwargs)


class FillContext(ClosedPathContext):
    """A drawing context that will apply a fill to any paths all objects in the
    context.

    The fill can use either the `Non-Zero
    <https://en.wikipedia.org/wiki/Nonzero-rule>`__ or `Even-Odd
    <https://en.wikipedia.org/wiki/Even-odd_rule>`__ winding rule for filling paths.

    This is a context manager; it creates a new path, and moves to the start coordinate;
    when the context exits, the path is closed with a fill. For fine-grained control of
    a path, you can use :class:`~toga.widgets.canvas.Context.begin_path`,
    :class:`~toga.widgets.canvas.Context.move_to`,
    :class:`~toga.widgets.canvas.Context.close_path` and
    :class:`~toga.widgets.canvas.Context.fill`.

    If both an x and y coordinate is provided, the drawing context will begin with
    a ``move_to`` operation in that context.

    You should not create a :class:`~toga.widgets.canvas.FillContext` context directly;
    instead, you should use the :meth:`~toga.widgets.canvas.Context.Fill` method on an
    existing context.
    """

    def __init__(
        self,
        canvas: toga.Canvas,
        x: float | None = None,
        y: float | None = None,
        color: str = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
    ):
        super().__init__(canvas=canvas, x=x, y=y)
        self.color = color
        self.fill_rule = fill_rule

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"color={self.color!r}, fill_rule={self.fill_rule})"
        )

    def _draw(self, impl, **kwargs):
        impl.push_context(**kwargs)
        impl.begin_path(**kwargs)
        if self.x is not None and self.y is not None:
            impl.move_to(x=self.x, y=self.y, **kwargs)

        sub_kwargs = kwargs.copy()
        sub_kwargs.update(fill_color=self.color, fill_rule=self.fill_rule)
        for obj in self.drawing_objects:
            obj._draw(impl, **sub_kwargs)

        # Fill passes fill_rule to its children; but that is also a valid argument for
        # fill(), so if a fill context is a child of a fill context, there's an argument
        # collision. Duplicate the kwargs and explicitly overwrite to avoid the
        # collision.
        draw_kwargs = kwargs.copy()
        draw_kwargs.update(fill_rule=self.fill_rule)
        impl.fill(self.color, **draw_kwargs)

        impl.pop_context(**kwargs)

    @property
    def color(self) -> Color:
        """The fill color."""
        return self._color

    @color.setter
    def color(self, value: Color | str | None):
        if value is None:
            self._color = parse_color(BLACK)
        else:
            self._color = parse_color(value)


class StrokeContext(ClosedPathContext):
    """Construct a drawing context that will draw a stroke on all paths defined
    within the context.

    This is a context manager; it creates a new path, and moves to the start coordinate;
    when the context exits, the path is drawn with the stroke. For fine-grained control of
    a path, you can use :class:`~toga.widgets.canvas.Context.begin_path`,
    :class:`~toga.widgets.canvas.Context.move_to`,
    :class:`~toga.widgets.canvas.Context.close_path` and
    :class:`~toga.widgets.canvas.Context.stroke`.

    If both an x and y coordinate is provided, the drawing context will begin with
    a ``move_to`` operation in that context.

    You should not create a :class:`~toga.widgets.canvas.StrokeContext` context directly;
    instead, you should use the :meth:`~toga.widgets.canvas.Context.Stroke` method on
    an existing context.
    """

    def __init__(
        self,
        canvas: toga.Canvas,
        x: float | None = None,
        y: float | None = None,
        color: str | None = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        super().__init__(canvas=canvas, x=x, y=y)
        self.color = color
        self.line_width = line_width
        self.line_dash = line_dash

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, color={self.color!r}, "
            f"line_width={self.line_width}, line_dash={self.line_dash!r})"
        )

    def _draw(self, impl, **kwargs):
        impl.push_context(**kwargs)
        impl.begin_path(**kwargs)

        if self.x is not None and self.y is not None:
            impl.move_to(x=self.x, y=self.y, **kwargs)

        sub_kwargs = kwargs.copy()
        sub_kwargs["stroke_color"] = self.color
        sub_kwargs["line_width"] = self.line_width
        sub_kwargs["line_dash"] = self.line_dash
        for obj in self.drawing_objects:
            obj._draw(impl, **sub_kwargs)

        # Stroke passes line_width and line_dash to its children; but those two are also
        # valid arguments for stroke, so if a stroke context is a child of stroke
        # context, there's an argument collision. Duplicate the kwargs and explicitly
        # overwrite to avoid the collision
        draw_kwargs = kwargs.copy()
        draw_kwargs["line_width"] = self.line_width
        draw_kwargs["line_dash"] = self.line_dash
        impl.stroke(self.color, **draw_kwargs)

        impl.pop_context(**kwargs)

    @property
    def color(self) -> Color:
        """The color of the stroke."""
        return self._color

    @color.setter
    def color(self, value):
        if value is None:
            self._color = parse_color(BLACK)
        else:
            self._color = parse_color(value)


#######################################################################################
# Events
#######################################################################################


class OnTouchHandler(Protocol):
    def __call__(self, widget: Canvas, x: int, y: int, **kwargs):
        """A handler that will be invoked when a :any:`Canvas` is touched with a finger
        or mouse.

        :param widget: The canvas that was touched.
        :param x: X coordinate, relative to the left edge of the canvas.
        :param y: Y coordinate, relative to the top edge of the canvas.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """
        ...


class OnResizeHandler(Protocol):
    def __call__(self, widget: Canvas, width: int, height: int, **kwargs):
        """A handler that will be invoked when a :any:`Canvas` is resized.

        :param widget: The canvas that was resized.
        :param width: The new width.
        :param height: The new height.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """
        ...


#######################################################################################
# The Canvas Widget
#######################################################################################


class Canvas(Widget):
    _MIN_WIDTH = 0
    _MIN_HEIGHT = 0

    def __init__(
        self,
        id=None,
        style=None,
        on_resize: OnResizeHandler = None,
        on_press: OnTouchHandler = None,
        on_activate: OnTouchHandler = None,
        on_release: OnTouchHandler = None,
        on_drag: OnTouchHandler = None,
        on_alt_press: OnTouchHandler = None,
        on_alt_release: OnTouchHandler = None,
        on_alt_drag: OnTouchHandler = None,
    ):
        """Create a new Canvas widget.

        Inherits from :class:`toga.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param on_resize: Initial :any:`on_resize` handler.
        :param on_press: Initial :any:`on_press` handler.
        :param on_activate: Initial :any:`on_activate` handler.
        :param on_release: Initial :any:`on_release` handler.
        :param on_drag: Initial :any:`on_drag` handler.
        :param on_alt_press: Initial :any:`on_alt_press` handler.
        :param on_alt_release: Initial :any:`on_alt_release` handler.
        :param on_alt_drag: Initial :any:`on_alt_drag` handler.
        """

        super().__init__(id=id, style=style)

        self._context = Context(canvas=self)

        # Create a platform specific implementation of Canvas
        self._impl = self.factory.Canvas(interface=self)

        # Set all the properties
        self.on_resize = on_resize
        self.on_press = on_press
        self.on_activate = on_activate
        self.on_release = on_release
        self.on_drag = on_drag
        self.on_alt_press = on_alt_press
        self.on_alt_release = on_alt_release
        self.on_alt_drag = on_alt_drag

    @property
    def enabled(self) -> bool:
        """Is the widget currently enabled? i.e., can the user interact with the widget?
        ScrollContainer widgets cannot be disabled; this property will always return
        True; any attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value):
        pass

    def focus(self):
        "No-op; ScrollContainer cannot accept input focus"
        pass

    @property
    def context(self) -> Context:
        """The root context for the canvas."""
        return self._context

    def redraw(self):
        """Redraw the Canvas.

        The Canvas will be automatically redrawn after adding or removing a drawing
        object, or when the Canvas resizes. However, when you modify the properties of a
        drawing object, you must call ``redraw`` manually.
        """
        self._impl.redraw()

    def Context(self):
        """Construct and yield a new sub-:class:`~toga.widgets.canvas.Context` within
        the root context of this Canvas.

        :yields: The new :class:`~toga.widgets.canvas.Context` object.
        """
        return self.context.Context()

    def ClosedPath(self, x: float | None = None, y: float | None = None):
        """Construct and yield a new :class:`~toga.widgets.canvas.ClosedPathContext` context in
        the root context of this canvas.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :yields: The new :class:`~toga.widgets.canvas.ClosedPathContext` context object.
        """
        return self.context.ClosedPath(x, y)

    def Fill(
        self,
        x: float | None = None,
        y: float | None = None,
        color: Color | str | None = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
    ):
        """Construct and yield a new :class:`~toga.widgets.canvas.FillContext` in the
        root context of this canvas.

        A drawing operator that fills the path constructed in the context according to
        the current fill rule.

        If both an x and y coordinate is provided, the drawing context will begin with
        a ``move_to`` operation in that context.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :param fill_rule: `nonzero` is the non-zero winding rule; `evenodd` is the
            even-odd winding rule.
        :param color: The fill color.
        :yields: The new :class:`~toga.widgets.canvas.FillContext` context object.
        """
        return self.context.Fill(x, y, color, fill_rule)

    def Stroke(
        self,
        x: float | None = None,
        y: float | None = None,
        color: Color | str | None = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        """Construct and yield a new :class:`~toga.widgets.canvas.StrokeContext` in the
        root context of this canvas.

        If both an x and y coordinate is provided, the drawing context will begin with
        a ``move_to`` operation in that context.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :param color: The color for the stroke.
        :param line_width: The width of the stroke.
        :param line_dash: The dash pattern to follow when drawing the line. Default is a
            solid line.
        :yields: The new :class:`~toga.widgets.canvas.StrokeContext` context object.
        """
        return self.context.Stroke(x, y, color, line_width, line_dash)

    @property
    def on_resize(self) -> OnResizeHandler:
        """The handler to invoke when the canvas is resized."""
        return self._on_resize

    @on_resize.setter
    def on_resize(self, handler: OnResizeHandler):
        self._on_resize = wrapped_handler(self, handler)

    @property
    def on_press(self) -> OnTouchHandler:
        """The handler invoked when the canvas is pressed. When a mouse is being used,
        this press will be with the primary (usually the left) mouse button."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler: OnTouchHandler):
        self._on_press = wrapped_handler(self, handler)

    @property
    def on_activate(self) -> OnTouchHandler:
        """The handler invoked when the canvas is pressed in a way indicating the
        pressed object should be activated. When a mouse is in use, this will usually be
        a double click with the primary (usually the left) mouse button.

        This event is not supported on Android or iOS."""
        return self._on_activate

    @on_activate.setter
    def on_activate(self, handler: OnTouchHandler):
        self._on_activate = wrapped_handler(self, handler)

    @property
    def on_release(self) -> OnTouchHandler:
        """The handler invoked when a press on the canvas ends."""
        return self._on_release

    @on_release.setter
    def on_release(self, handler: OnTouchHandler):
        self._on_release = wrapped_handler(self, handler)

    @property
    def on_drag(self) -> OnTouchHandler:
        """The handler invoked when the location of a press changes."""
        return self._on_drag

    @on_drag.setter
    def on_drag(self, handler: OnTouchHandler):
        self._on_drag = wrapped_handler(self, handler)

    @property
    def on_alt_press(self) -> OnTouchHandler:
        """The handler to invoke when the canvas is pressed in an alternate
        manner. This will usually correspond to a secondary (usually the right) mouse
        button press.

        This event is not supported on Android or iOS.
        """
        return self._on_alt_press

    @on_alt_press.setter
    def on_alt_press(self, handler: OnTouchHandler):
        self._on_alt_press = wrapped_handler(self, handler)

    @property
    def on_alt_release(self) -> OnTouchHandler:
        """The handler to invoke when an alternate press is released.

        This event is not supported on Android or iOS.
        """
        return self._on_alt_release

    @on_alt_release.setter
    def on_alt_release(self, handler: OnTouchHandler):
        self._on_alt_release = wrapped_handler(self, handler)

    @property
    def on_alt_drag(self) -> OnTouchHandler:
        """The handler to invoke when the location of an alternate press changes.

        This event is not supported on Android or iOS.
        """
        return self._on_alt_drag

    @on_alt_drag.setter
    def on_alt_drag(self, handler: OnTouchHandler):
        self._on_alt_drag = wrapped_handler(self, handler)

    ###########################################################################
    # Text measurement
    ###########################################################################

    def measure_text(
        self,
        text: str,
        font: Font | None = None,
        tight=None,  # DEPRECATED
    ) -> tuple[float, float]:
        """Measure the size at which :meth:`~.Context.write_text` would render some text.

        :param text: The text to measure. Newlines will cause line breaks, but long
            lines will not be wrapped.
        :param font: The font in which to draw the text. The default is the system font.
        :param tight: **DEPRECATED**: this argument has no effect.
        :returns: A tuple of ``(width, height)``.
        """
        if tight is not None:
            warnings.warn(
                "The `tight` argument on Canvas.measure_text() has been deprecated.",
                DeprecationWarning,
            )
        if font is None:
            font = Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE)

        return self._impl.measure_text(str(text), font._impl)

    ###########################################################################
    # As image
    ###########################################################################

    def as_image(self, format: type[ImageT] = toga.Image) -> ImageT:
        """Render the canvas as an image.

        :param format: Format to provide. Defaults to :class:`~toga.images.Image`; also
            supports :class:`PIL.Image.Image` if Pillow is installed
        :returns: The canvas as an image of the specified type.
        """
        return toga.Image(self._impl.get_image_data()).as_format(format)

    ###########################################################################
    # 2023-07 Backwards compatibility
    ###########################################################################

    def new_path(self):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.begin_path` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.begin_path()",
            DeprecationWarning,
        )
        return self.context.begin_path()

    def move_to(self, x, y):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.move_to` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.move_to()",
            DeprecationWarning,
        )
        return self.context.move_to(x, y)

    def line_to(self, x, y):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.line_to` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.line_to()",
            DeprecationWarning,
        )
        return self.context.line_to(x, y)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.bezier_curve_to` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.bezier_curve_to()",
            DeprecationWarning,
        )
        return self.context.bezier_curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx: float, cpy: float, x: float, y: float):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.quadratic_curve_to`
        on :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.quadratic_curve_to()",
            DeprecationWarning,
        )
        return self.context.quadratic_curve_to(cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.arc` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.arc()",
            DeprecationWarning,
        )
        return self.context.arc(x, y, radius, startangle, endangle, anticlockwise)

    def ellipse(
        self,
        x: float,
        y: float,
        radiusx: float,
        radiusy: float,
        rotation: float = 0.0,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        anticlockwise: bool = False,
    ):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.ellipse` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.ellipse()",
            DeprecationWarning,
        )
        return self.context.ellipse(
            x,
            y,
            radiusx,
            radiusy,
            rotation,
            startangle,
            endangle,
            anticlockwise,
        )

    def rect(self, x: float, y: float, width: float, height: float):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.rect` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.rect()",
            DeprecationWarning,
        )
        return self.context.rect(x, y, width, height)

    def write_text(self, text: str, x=0, y=0, font=None):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.write_text` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.write_text()",
            DeprecationWarning,
        )
        return self.context.write_text(text, x, y, font)

    def rotate(self, radians: float):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.rotate` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.rotate()",
            DeprecationWarning,
        )
        return self.context.rotate(radians)

    def scale(self, sx: float, sy: float):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.scale` on :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.scale()",
            DeprecationWarning,
        )
        return self.context.scale(sx, sy)

    def translate(self, tx: float, ty: float):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.translate` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.translate()",
            DeprecationWarning,
        )
        return self.context.translate(tx, ty)

    def reset_transform(self):
        """**DEPRECATED** - Use :meth:`~toga.widgets.canvas.Context.reset_transform` on
        :attr:`context`"""
        warnings.warn(
            "Direct canvas operations have been deprecated; use context.reset_transform()",
            DeprecationWarning,
        )
        return self.context.reset_transform()

    def closed_path(self, x, y):
        """**DEPRECATED** - use :meth:`~toga.Canvas.ClosedPath`"""
        warnings.warn(
            "Canvas.closed_path() has been renamed Canvas.ClosedPath()",
            DeprecationWarning,
        )
        return self.ClosedPath(x, y)

    def fill(
        self,
        color: Color | str | None = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
        preserve=None,  # DEPRECATED
    ):
        """**DEPRECATED** - use :meth:`~toga.Canvas.Fill`"""
        warnings.warn(
            "Canvas.fill() has been renamed Canvas.Fill()",
            DeprecationWarning,
        )
        if preserve is not None:
            warnings.warn(
                "The `preserve` argument on fill() has been deprecated.",
                DeprecationWarning,
            )
        return self.Fill(color=color, fill_rule=fill_rule)

    def stroke(
        self,
        color: Color | str | None = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        """**DEPRECATED** - use :meth:`~toga.Canvas.Stroke`"""
        warnings.warn(
            "Canvas.stroke() has been renamed Canvas.Stroke().",
            DeprecationWarning,
        )
        return self.Stroke(color=color, line_width=line_width, line_dash=line_dash)


def sweepangle(startangle, endangle, anticlockwise):
    """Returns an arc length in the range [-2 * pi, 2 * pi], where positive numbers are
    clockwise. Based on the "ellipse method steps" in the HTML spec."""

    if anticlockwise:
        if endangle - startangle <= -2 * pi:
            return -2 * pi
    else:
        if endangle - startangle >= 2 * pi:
            return 2 * pi

    startangle %= 2 * pi
    endangle %= 2 * pi
    sweepangle = endangle - startangle
    if anticlockwise:
        if sweepangle > 0:
            sweepangle -= 2 * pi
    else:
        if sweepangle < 0:
            sweepangle += 2 * pi

    return sweepangle


# Based on https://stackoverflow.com/a/30279817
def arc_to_bezier(sweepangle):
    """Approximates an arc of a unit circle as a sequence of Bezier segments.

    :param sweepangle: Length of the arc in radians, where positive numbers are
        clockwise.
    :returns: [(1, 0), (cp1x, cp1y), (cp2x, cp2y), (x, y), ...], where each group of 3
        points has the same meaning as in the bezier_curve_to method, and there are
        between 1 and 4 groups."""

    matrices = [
        [1, 0, 0, 1],  # 0 degrees
        [0, -1, 1, 0],  # 90
        [-1, 0, 0, -1],  # 180
        [0, 1, -1, 0],  # 270
    ]

    if sweepangle < 0:  # Anticlockwise
        sweepangle *= -1
        for matrix in matrices:
            matrix[2] *= -1
            matrix[3] *= -1

    result = [(1.0, 0.0)]
    for matrix in matrices:
        if sweepangle < 0:
            break

        phi = min(sweepangle, pi / 2)
        k = 4 / 3 * tan(phi / 4)
        result += [
            transform(x, y, matrix)
            for x, y in [
                (1, k),
                (cos(phi) + k * sin(phi), sin(phi) - k * cos(phi)),
                (cos(phi), sin(phi)),
            ]
        ]

        sweepangle -= pi / 2

    return result


def transform(x, y, matrix):
    return (
        x * matrix[0] + y * matrix[1],
        x * matrix[2] + y * matrix[3],
    )
