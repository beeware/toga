from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from contextlib import contextmanager
from math import pi

import toga
from toga.colors import BLACK, color as parse_color
from toga.constants import FillRule
from toga.fonts import SYSTEM, Font
from toga.handlers import wrapped_handler

from .. import Image
from .base import Widget

#######################################################################################
# Simple drawing objects
#######################################################################################


class DrawingObject(ABC):
    """A base class for drawing objects."""

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def _draw(self, impl, **kwargs):
        ...


class BeginPath(DrawingObject):
    """A drawing object that starts a new path."""

    def _draw(self, impl, **kwargs):
        impl.begin_path(**kwargs)


class ClosePath(DrawingObject):
    """A drawing object that closes the current path."""

    def _draw(self, impl, **kwargs):
        impl.close_path(**kwargs)


class MoveTo(DrawingObject):
    def __init__(self, x, y):
        """A drawing object that moves the current point of the canvas context without
        drawing.

        :param x: The x coordinate  of the new current point.
        :param y: The y coordinate of the new current point.
        """
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl, **kwargs):
        """Draw the drawing object using the implementation."""
        impl.move_to(self.x, self.y, **kwargs)


class LineTo(DrawingObject):
    def __init__(self, x, y):
        """A drawing object that draws a line segment ending at a point in the canvas
        context.

        :param x: The x coordinate for the end point of the line segment.
        :param y: The y coordinate for the end point of the line segment.
        """
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl, **kwargs):
        impl.line_to(self.x, self.y, **kwargs)


class BezierCurveTo(DrawingObject):
    def __init__(self, cp1x, cp1y, cp2x, cp2y, x, y):
        """A drawing object that draws a Bezier curve in the canvas context.

        A Bézier curve requires three points. The first two are control points; the
        third is the end point for the curve. The starting point is the last point in
        the current path, which can be changed using move_to() before creating the
        Bézier curve.

        :param cp1y: The y coordinate for the first control point of the Bezier curve.
        :param cp1x: The x coordinate for the first control point of the Bezier curve.
        :param cp2x: The x coordinate for the second control point of the Bezier curve.
        :param cp2y: The y coordinate for the second control point of the Bezier curve.
        :param x: The x coordinate for the end point.
        :param y: The y coordinate for the end point.
        """
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
    def __init__(self, cpx, cpy, x, y):
        """A drawing object that draws a quadratic curve in the canvas context.

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
        """
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
        x,
        y,
        radius,
        startangle=0.0,
        endangle=2 * pi,
        anticlockwise=False,
    ):
        """A drawing object that draws a circular arc in the canvas context.

        A full circle will be drawn by default; an arc can be drawn by
        specifying a start and end angle. By default, the arc will be drawn from the
        start angle to the end angle, sweeping clockwise.

        :param x: The x axis of the coordinate for the ellipse's center.
        :param y: The y axis of the coordinate for the ellipse's center.
        :param startangle: The starting angle in radians, measured from the positive x
            axis.
        :param endangle: The end angle in radians, measured from the positive x axis.
        :param anticlockwise: The direction in which to sweep the arc from start angle
            to end angle.
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"radius={self.radius}, startangle={self.startangle}, "
            f"endangle={self.endangle}, anticlockwise={self.anticlockwise})"
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
        x,
        y,
        radiusx,
        radiusy,
        rotation=0.0,
        startangle=0.0,
        endangle=2 * pi,
        anticlockwise=False,
    ):
        """A drawing object that draws an ellipse in the canvas context.

        A full ellipse will be drawn by default; an elliptical arc can be drawn by
        specifying a start and end angle. By default, the elliptical arc will be drawn
        from the start angle to the end angle, sweeping clockwise.

        :param x: The x axis of the coordinate for the ellipse's center.
        :param y: The y axis of the coordinate for the ellipse's center.
        :param radiusx: The ellipse's major axis radius.
        :param radiusy: The ellipse's minor axis radius.
        :param rotation: The rotation for this ellipse, expressed in radians.
        :param startangle: The starting angle in radians, measured from the positive x
            axis.
        :param endangle: The end angle in radians, measured from the positive x axis.
        :param anticlockwise: The direction in which to sweep the elliptical arc from
            start angle to end angle.
        """
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
            f"rotation={self.rotation}, startangle={self.startangle}, endangle={self.endangle}, "
            f"anticlockwise={self.anticlockwise})"
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
    def __init__(self, x, y, width, height):
        """A drawing object that draws a rectangle in the canvas context.

        :param x: The horizontal coordinate of the left of the rectangle.
        :param y: The vertical coordinate of the top of the rectangle.
        :param width: The width of the rectangle.
        :param hegiht: The height of the rectangle.
        """
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
    def __init__(self, text, x, y, font):
        """A drawing object that write texts at a given position in the canvas context.

        If no font is specified, it will be drawn in the system font.

        Drawing text is effectively a series of stroke operations, so the text will have
        the color and fill properties of the canvas context.

        :param text: The text to write.
        :param x: The x coordinate of the top left corner of the text's bounding
            rectangle.
        :param y: The y coordinate of the top left corner of the text's bounding
            rectangle.
        :param font: The font in which to draw the text.
        """
        self.text = text
        self.x = x
        self.y = y
        self.font = font

    def __repr__(self):
        return f"{self.__class__.__name__}(text={self.text!r}, x={self.x}, y={self.y}, font={self.font!r})"

    def _draw(self, impl, **kwargs):
        impl.write_text(self.text, self.x, self.y, self.font._impl, **kwargs)


class Rotate(DrawingObject):
    def __init__(self, radians):
        """A drawing operation that adds a rotation to the canvas context.

        :param radians:: The angle to rotate clockwise in radians.
        :returns: The :class:`Rotate` drawing object for the transformation.
        """
        self.radians = radians

    def __repr__(self):
        return f"{self.__class__.__name__}(radians={self.radians})"

    def _draw(self, impl, **kwargs):
        impl.rotate(self.radians, **kwargs)


class Scale(DrawingObject):
    def __init__(self, sx, sy):
        """A drawing operation that adds a scaling transformation to the canvas context.

        :param sx: scale factor for the X dimension.
        :param sy: scale factor for the Y dimension.
        """
        self.sx = sx
        self.sy = sy

    def __repr__(self):
        return f"{self.__class__.__name__}(sx={self.sx}, sy={self.sy})"

    def _draw(self, impl, **kwargs):
        impl.scale(self.sx, self.sy, **kwargs)


class Translate(DrawingObject):
    def __init__(self, tx, ty):
        """A drawing operation that adds a translation to the canvas context.

        :param tx: Size of the X value of coordinate.
        :param ty: Y value of coordinate.
        """
        self.tx = tx
        self.ty = ty

    def __repr__(self):
        return f"{self.__class__.__name__}(tx={self.tx}, ty={self.ty})"

    def _draw(self, impl, **kwargs):
        impl.translate(self.tx, self.ty, **kwargs)


class ResetTransform(DrawingObject):
    """Reset all transformations in the canvas context."""

    def _draw(self, impl, **kwargs):
        impl.reset_transform(**kwargs)


#######################################################################################
# Drawing Contexts
#######################################################################################


class Context(DrawingObject):
    """A drawing context for a canvas.

    You should not create a :class:`~toga.widgets.canvas.Context` directly; instead, you should use a
    the :meth:`~toga.widgets.canvas.Context.context` method on an existing context,
    or use :attr:`toga.Canvas.context` to access the root context of the canvas.
    """

    def __init__(self, canvas, context=None, **kwargs):
        # kwargs used to support multiple inheritance
        super().__init__(**kwargs)
        self._canvas = canvas
        self._context = None
        self.drawing_objects = []

    def _draw(self, impl, **kwargs):
        # impl.push_context(**kwargs)
        for obj in self.drawing_objects:
            obj._draw(impl, **kwargs)
        # impl.pop_context(**kwargs)

    ###########################################################################
    # Methods to keep track of the canvas, automatically redraw it
    ###########################################################################

    @property
    def canvas(self) -> Canvas:
        """The canvas that is associated with this drawing context."""
        return self._canvas

    def redraw(self):
        """Force a redraw of the Canvas.

        The Canvas will be automatically redrawn after adding or remove a drawing
        object. If you modify a drawing object, this method is used to force a redraw.
        """
        self.canvas._impl.redraw()

    ###########################################################################
    # Operations on drawing objects
    ###########################################################################

    def append(self, obj: DrawingObject) -> DrawingObject:
        """Append a drawing object to the context.

        :param obj: The drawing object to add to the context.
        """
        self.drawing_objects.append(obj)
        self.redraw()

    def insert(self, index: int, obj: DrawingObject) -> DrawingObject:
        """Insert a drawing object into the context at a specific index.

        :param index: The index at which the drawing object should be inserted.
        :param obj: The drawing object to add to the context.
        """
        self.drawing_objects.insert(index, obj)
        self.redraw()

    def remove(self, obj):
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

        :returns: The :class:`~toga.widgets.canvas.BeginPath` drawing object for the
            operation.
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

        :returns: The :class:`~toga.widgets.canvas.ClosePath` drawing object for the
            operation.
        """
        close_path = ClosePath()
        self.append(close_path)
        return close_path

    def move_to(self, x, y):
        """Moves the current point of the canvas context without drawing.

        :param x: The x coordinate of the new current point.
        :param y: The y coordinate of the new current point.
        :returns: The :class:`~toga.widgets.canvas.MoveTo` drawing object for the
            operation.
        """
        move_to = MoveTo(x, y)
        self.append(move_to)
        return move_to

    def line_to(self, x, y):
        """Draw a line segment ending at a point in the canvas context.

        :param x: The x coordinate for the end point of the line segment.
        :param y: The y coordinate for the end point of the line segment.
        :returns: The :class:`~toga.widgets.canvas.LineTo` drawing object for the
            operation.
        """
        line_to = LineTo(x, y)
        self.append(line_to)
        return line_to

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        """Draw a Bezier curve in the canvas context.

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
        :returns: The :class:`~toga.widgets.canvas.BezierCurveTo` drawing object for the
            operation.
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
        :returns: The :class:`~toga.widgets.canvas.QuadraticCurveTo` drawing object for
            the operation.
        """
        quadratic_curve_to = QuadraticCurveTo(cpx, cpy, x, y)
        self.append(quadratic_curve_to)
        return quadratic_curve_to

    def arc(self, x, y, radius, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        """Draw a circular arc in the canvas context.

        A full circle will be drawn by default; an arc can be drawn by specifying a
        start and end angle. By default, the arc will be drawn from the start angle to
        the end angle, sweeping clockwise.

        :param x: The x axis of the coordinate for the ellipse's center.
        :param y: The y axis of the coordinate for the ellipse's center.
        :param startangle: The starting angle in radians, measured from the positive x
            axis.
        :param endangle: The end angle in radians, measured from the positive x axis.
        :param anticlockwise: The direction in which to sweep the arc from start angle
            to end angle.
        :returns: The :class:`~toga.widgets.canvas.Arc` drawing object for the
            operation.
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
        """Draw an ellipse in the canvas context.

        A full ellipse will be drawn by default; an elliptical arc can be drawn by
        specifying a start and end angle. By default, the elliptical arc will be drawn
        from the start angle to the end angle, sweeping clockwise.

        :param x: The x axis of the coordinate for the ellipse's center.
        :param y: The y axis of the coordinate for the ellipse's center.
        :param radiusx: The ellipse's major axis radius.
        :param radiusy: The ellipse's minor axis radius.
        :param rotation: The rotation for this ellipse, expressed in radians.
        :param startangle: The starting angle in radians, measured from the positive x
            axis.
        :param endangle: The end angle in radians, measured from the positive x axis.
        :param anticlockwise: The direction in which to sweep the elliptical arc from
            start angle to end angle.
        :returns: The :class:`~toga.widgets.canvas.Ellipse` drawing object for the
            operation.
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
        :param hegiht: The height of the rectangle.
        :returns: The :class:`~toga.widgets.canvas.Rect` drawing object for the
            operation.
        """
        rect = Rect(x, y, width, height)
        self.append(rect)
        return rect

    ###########################################################################
    # Text drawing
    ###########################################################################

    def write_text(self, text: str, x=0, y=0, font=None):
        """Write text at a given position in the canvas context.

        If no font is specified, it will be drawn in the system font.

        Drawing text is effectively a series of stroke operations, so the text will have
        the color and fill properties of the canvas context.

        :param text: The text to write.
        :param x: The x coordinate of the top left corner of the text's bounding
            rectangle.
        :param y: The y coordinate of the top left corner of the text's bounding
            rectangle.
        :param font: The font in which to draw the text.
        :returns: The :class:`~toga.widgets.canvas.WriteText` drawing object for the
            operation.
        """
        if font is None:
            font = Font(family=SYSTEM, size=self._canvas.style.font_size)
        write_text = WriteText(str(text), x, y, font)
        self.append(write_text)
        return write_text

    ###########################################################################
    # Transformations
    ###########################################################################
    def rotate(self, radians: float):
        """Add a rotation to the canvas context.

        :param radians:: The angle to rotate clockwise in radians.
        :returns: The :class:`~toga.widgets.canvas.Rotate` drawing object for the
            transformation.
        """
        rotate = Rotate(radians)
        self.append(rotate)
        return rotate

    def scale(self, sx: float, sy: float):
        """Add a scaling transformation to the canvas context.

        :param sx: scale factor for the X dimension.
        :param sy: scale factor for the Y dimension.
        :returns: The :class:`~toga.widgets.canvas.Scale` drawing object for the
            transformation.
        """
        scale = Scale(sx, sy)
        self.append(scale)
        return scale

    def translate(self, tx: float, ty: float):
        """Add a translation to the canvas context.

        :param tx: Size of the X value of coordinate.
        :param ty: Y value of coordinate.
        :returns: The :class:`~toga.widgets.canvas.Translate` drawing object for the
            transformation.
        """
        translate = Translate(tx, ty)
        self.append(translate)
        return translate

    def reset_transform(self):
        """Reset all transformations in the canvas context.

        :returns: The :class:`~toga.widgets.canvas.ResetTransform` drawing object for
            the reset.
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
        context = Context(canvas=self._canvas, context=self)
        self.append(context)
        yield context
        self.redraw()

    @contextmanager
    def ClosedPath(self, x: float, y: float):
        """Construct and yield a new :class:`~toga.widgets.canvas.ClosedPath`
        sub-context that will draw a closed path, starting from an origin.

        This is a context manager; it creates a new path and moves to the start
        coordinate; when the context exits, the path is closed. For fine-grained control
        of a path, you can use :meth:`~toga.widgets.canvas.Context.begin_path` and
        :meth:`~toga.widgets.canvas.Context.close_path` simple operations.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :yields: The :class:`~toga.widgets.canvas.ClosedPath` context object.
        """
        closed_path = ClosedPath(canvas=self.canvas, context=self, x=x, y=y)
        closed_path._canvas = self.canvas
        self.append(closed_path)
        yield closed_path
        self.redraw()

    @contextmanager
    def Fill(
        self,
        color: str = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
    ):
        """Construct and yield a new :class:`~toga.widgets.canvas.Fill` sub-context
        within this context.

        A drawing operator that fills the path constructed in the context according to
        the current fill rule.

        :param fill_rule: `nonzero` is the non-zero winding rule; `evenodd` is the
            even-odd winding rule.
        :param color: The fill color.
        :yields: The new :class:`~toga.widgets.canvas.Fill` context object.
        """
        fill = Fill(canvas=self.canvas, context=self, color=color, fill_rule=fill_rule)
        self.append(fill)
        yield fill
        self.redraw()

    @contextmanager
    def Stroke(
        self,
        color: str = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        """Construct and yield a new :class:`~toga.widgets.canvas.Stroke` sub-context
        within this context.

        :param color: The color for the stroke.
        :param line_width: The width of the stroke.
        :param line_dash: The dash pattern to follow when drawing the line. Default is a
            solid line.
        :yields: The new :class:`~toga.widgets.canvas.Stroke` context object.
        """
        stroke = Stroke(
            canvas=self.canvas,
            context=self,
            color=color,
            line_width=line_width,
            line_dash=line_dash,
        )
        self.append(stroke)
        yield stroke
        self.redraw()

    ###########################################################################
    # 2023-07 Backwards incompatibility
    ###########################################################################

    def new_path(self):
        """**DEPRECATED** - Use :meth:`~toga.canvas.widgets.Context.begin_path`."""
        warnings.warn("Context.new_path() has been renamed Context.begin_path()")
        return self.begin_path()

    def context(self):
        """**DEPRECATED** - use :meth:`~toga.widgets.canvas.Context.Context`"""
        warnings.warn("Context.context() has been renamed Context.Context().")
        return self.Context()

    def closed_path(self, x: float, y: float):
        """**DEPRECATED** - use :meth:`~toga.widgets.canvas.Context.ClosedPath`"""
        warnings.warn("Context.closed_path() has been renamed Context.ClosedPath().")
        return self.ClosedPath(x, y)

    def fill(
        self,
        color: str = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
        preserve=None,
    ):
        """**DEPRECATED** - use :meth:`~toga.widgets.canvas.Context.Fill`"""
        warnings.warn("Context.fill() has been renamed Context.Fill().")
        if preserve is not None:
            warnings.warn("The `preserve` argument on fill() has been deprecated.")
        return self.Fill(color, fill_rule)

    def stroke(
        self,
        color: str = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        """**DEPRECATED** - use :meth:`~toga.widgets.canvas.Context.Stroke`"""
        warnings.warn("Context.stroke() has been renamed Context.Stroke().")
        return self.Stroke(color, line_width, line_dash)


class ClosedPath(Context):
    """A drawing context that will build a closed path, starting from an
    origin.

    This is a context manager; it creates a new path and moves to the start coordinate;
    when the context exits, the path is closed. For fine-grained control of a path, you
    can use :class:`~toga.widgets.canvas.Context.begin_path`,
    :class:`~toga.widgets.canvas.Context.move_to` and
    :class:`~toga.widgets.canvas.Context.close_path` primitives.

    You should not create a :class:`~toga.widgets.canvas.ClosedPath` context directly;
    instead, you should use a the :meth:`~toga.widgets.canvas.Context.closedpath` method
    on an existing context.
    """

    def __init__(
        self,
        canvas: toga.Canvas,
        context: Context,
        x: float,
        y: float,
    ):
        super().__init__(canvas=canvas, context=context)
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl, **kwargs):
        """Used by parent to draw all objects that are part of the context."""
        # impl.begin_path(**kwargs)
        impl.move_to(x=self.x, y=self.y, **kwargs)
        for obj in self.drawing_objects:
            obj._draw(impl, **kwargs)
        impl.close_path(x=self.x, y=self.y, **kwargs)

    @property
    def x(self) -> float:
        """The x coordinate of the path's starting point."""
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = float(value)

    @property
    def y(self) -> float:
        """The y coordinate of the path's starting point."""
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = float(value)


class Fill(Context):
    """A drawing context that will apply a fill to any paths all objects in the
    context.

    The fill can use either the `Non-Zero
    <https://en.wikipedia.org/wiki/Nonzero-rule>`__ or `Even-Odd
    <https://en.wikipedia.org/wiki/Even-odd_rule>`__ winding rule for filling paths.

    You should not create a :class:`~toga.widgets.canvas.Fill` context directly;
    instead, you should use a the :meth:`~toga.widgets.canvas.Context.fill` method on an
    existing context.
    """

    def __init__(
        self,
        canvas: toga.Canvas,
        context: Context | None,
        color: str = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
    ):
        super().__init__(canvas=canvas, context=context)
        self.color = color
        self.fill_rule = fill_rule

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(color={self.color!r}, "
            f"fill_rule={self.fill_rule})"
        )

    def _draw(self, impl, **kwargs):
        impl.begin_path(**kwargs)
        for obj in self.drawing_objects:
            kwargs["fill_color"] = self.color
            obj._draw(impl, **kwargs)
        impl.fill(self.color, self.fill_rule, **kwargs)

    @property
    def fill_rule(self) -> FillRule:
        """The fill rule to use."""
        return self._fill_rule

    @fill_rule.setter
    def fill_rule(self, fill_rule: FillRule):
        self._fill_rule = fill_rule

    @property
    def color(self) -> str | None:
        """The fill color. Can be any valid CSS color value as a string."""
        return self._color

    @color.setter
    def color(self, value: str | None):
        if value is None:
            self._color = None
        else:
            self._color = parse_color(value)


class Stroke(Context):
    """Construct a drawing context that will draw a stroke on all paths defined
    within the context.

    You should not create a :class:`~toga.widgets.canvas.Stroke` context directly;
    instead, you should use a the :meth:`~toga.widgets.canvas.Context.stroke` method on
    an existing context.
    """

    def __init__(
        self,
        canvas: toga.Canvas,
        context: Context,
        color: str | None = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        super().__init__(canvas=canvas, context=context)
        self.color = color
        self.line_width = line_width
        self.line_dash = line_dash

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(color={self.color!r}, "
            f"line_width={self.line_width}, line_dash={self.line_dash!r})"
        )

    def _draw(self, impl, **kwargs):
        """Used by parent to draw all objects that are part of the context."""
        impl.begin_path(**kwargs)
        for obj in self.drawing_objects:
            kwargs["stroke_color"] = self.color
            kwargs["text_line_width"] = self.line_width
            kwargs["text_line_dash"] = self.line_dash
            obj._draw(impl, **kwargs)
        impl.stroke(self.color, self.line_width, self.line_dash, **kwargs)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value is None:
            self._color = None
        else:
            self._color = parse_color(value)


#######################################################################################
# The Canvas Widget
#######################################################################################


class Canvas(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        on_resize: callable = None,
        on_press: callable = None,
        on_release: callable = None,
        on_drag: callable = None,
        on_alt_press: callable = None,
        on_alt_release: callable = None,
        on_alt_drag: callable = None,
    ):
        """Create a new Canvas widget.

        Inherits from :class:`toga.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param on_resize: Initial :any:`on_resize` handler.
        :param on_press: Initial :any:`on_press` handler.
        :param on_release: Initial :any:`on_release` handler.
        :param on_drag: Initial :any:`on_drag` handler.
        :param on_alt_press: Initial :any:`on_alt_press` handler.
        :param on_alt_release: Initial :any:`on_alt_release` handler.
        :param on_alt_drag: Initial :any:`on_alt_drag` handler.
        """

        super().__init__(id=id, style=style)

        self._context = Context(canvas=self, context=None)

        # Create a platform specific implementation of Canvas
        self._impl = self.factory.Canvas(interface=self)

        # Set all the properties
        self.on_resize = on_resize
        self.on_press = on_press
        self.on_release = on_release
        self.on_drag = on_drag
        self.on_alt_press = on_alt_press
        self.on_alt_release = on_alt_release
        self.on_alt_drag = on_alt_drag

    @property
    def context(self) -> Context:
        """The root context for the canvas."""
        return self._context

    def clear(self):
        """Remove all drawing objects from the canvas."""
        return self._context.clear()

    def Context(self):
        """Construct and yield a new sub-:class:`~toga.widgets.canvas.Context` within
        this context.

        :yields: The new :class:`~toga.widgets.canvas.Context` object.
        """
        return self.context.Context()

    def Path(self, x: float, y: float):
        """Constructs and yield a new :class:`~toga.widgets.canvas.Path` context on the
        canvas, starting at an origin.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :yields: The :class:`~toga.widgets.canvas.Path` context object.
        """
        return self.context.Path(x, y)

    def ClosedPath(self, x: float, y: float):
        """Construct and yield a new :class:`~toga.widgets.canvas.ClosedPath` context on
        the canvas that will draw a closed path, starting from an origin.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :yields: The :class:`~toga.widgets.canvas.ClosedPath` context object.
        """
        return self.context.ClosedPath(x, y)

    def Fill(
        self,
        color: str = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
    ):
        """Construct and yield a new :class:`~toga.widgets.canvas.Fill` context on the
        canvas.

        A drawing operator that fills the path constructed in the context according to
        the current fill rule.

        :param fill_rule: `nonzero` is the non-zero winding rule; `evenodd` is the
            even-odd winding rule.
        :param color: The fill color.
        :yields: The new :class:`~toga.widgets.canvas.Fill` context object.
        """
        return self.context.Fill(color, fill_rule)

    def Stroke(
        self,
        color: str = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        """Construct and yield a new :class:`~toga.widgets.canvas.Stroke` sub-context within this canvas.

        :param color: The color for the stroke.
        :param line_width: The width of the stroke.
        :param line_dash: The dash pattern to follow when drawing the line. Default is a
            solid line.
        :yields: The new :class:`~toga.widgets.canvas.Stroke` context object.
        """
        return self.context.Stroke(color, line_width, line_dash)

    @property
    def on_resize(self) -> callable:
        """The handler to invoke when the canvas is resized."""
        return self._on_resize

    @on_resize.setter
    def on_resize(self, handler: callable):
        self._on_resize = wrapped_handler(self, handler)

    @property
    def on_press(self) -> callable:
        """The handler invoked when the primary (usually the left) mouse button
        is pressed."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler: callable):
        self._on_press = wrapped_handler(self, handler)

    @property
    def on_release(self) -> callable:
        """The handler invoked when the primary (usually the left) mouse button
        is released."""
        return self._on_release

    @on_release.setter
    def on_release(self, handler):
        self._on_release = wrapped_handler(self, handler)

    @property
    def on_drag(self) -> callable:
        """The handler invoked when the mouse is dragged with the primary
        (usually the left) mouse button."""
        return self._on_drag

    @on_drag.setter
    def on_drag(self, handler: callable):
        self._on_drag = wrapped_handler(self, handler)

    @property
    def on_alt_press(self) -> callable:
        """The handler to invoke when the alternate (usually the right) mouse button is
        pressed."""
        return self._on_alt_press

    @on_alt_press.setter
    def on_alt_press(self, handler: callable):
        self._on_alt_press = wrapped_handler(self, handler)

    @property
    def on_alt_release(self) -> callable:
        """Return the handler to invoke when the alternate (usually the right) mouse
        button is released."""
        return self._on_alt_release

    @on_alt_release.setter
    def on_alt_release(self, handler: callable):
        self._on_alt_release = wrapped_handler(self, handler)

    @property
    def on_alt_drag(self) -> callable:
        """Return the handler to invoke when the mouse is dragged with the alternate
        (usually the right) mouse button."""
        return self._on_alt_drag

    @on_alt_drag.setter
    def on_alt_drag(self, handler: callable):
        self._on_alt_drag = wrapped_handler(self, handler)

    ###########################################################################
    # Text measurement
    ###########################################################################

    def measure_text(self, text, font, tight=False):
        return self._impl.measure_text(text, font._impl, tight=tight)

    ###########################################################################
    # As image
    ###########################################################################

    def as_image(self) -> toga.Image:
        """Render the canvas as an Image.

        :returns: A :class:`toga.Image` containing the canvas content."""
        return Image(data=self._impl.get_image_data())

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
        return self.context.new_path()

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
        return self.context.write_text(x, y, width, height)

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
        warnings.warn("Canvas.closed_path() has been renamed Canvas.ClosedPath()")
        return self.ClosedPath(x, y)

    def fill(
        self,
        color: str = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
        preserve=None,  # DEPRECATED
    ):
        warnings.warn("Canvas.fill() has been renamed Canvas.Fill()")
        if preserve is not None:
            warnings.warn("The `preserve` argument on fill() has been deprecated.")
        return self.Fill(color, fill_rule)

    def stroke(
        self,
        color: str = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ):
        warnings.warn("Canvas.stroke() has been renamed Canvas.Stroke().")
        return self.Stroke(color, line_width, line_dash)
