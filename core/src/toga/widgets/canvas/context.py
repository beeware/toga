from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from math import pi
from typing import TYPE_CHECKING, Any

from travertino.colors import Color

import toga
from toga.colors import BLACK, color as parse_color
from toga.constants import Baseline, FillRule
from toga.fonts import Font

from .drawingobject import (
    Arc,
    BeginPath,
    BezierCurveTo,
    ClosePath,
    DrawingObject,
    Ellipse,
    Fill,
    LineTo,
    MoveTo,
    QuadraticCurveTo,
    Rect,
    ResetTransform,
    Rotate,
    Scale,
    Stroke,
    Translate,
    WriteText,
)

if TYPE_CHECKING:
    from .canvas import Canvas


class Context(DrawingObject):
    """A drawing context for a canvas.

    You should not create a :class:`~toga.widgets.canvas.Context` directly; instead,
    you should use the :meth:`~Context.Context` method on an existing context,
    or use :any:`Canvas.context` to access the root context of the canvas.
    """

    def __init__(self, canvas: toga.Canvas, **kwargs: Any):
        # kwargs used to support multiple inheritance
        super().__init__(**kwargs)
        self._canvas = canvas
        self.drawing_objects: list[DrawingObject] = []

    def _draw(self, impl: Any, **kwargs: Any) -> None:
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

    def redraw(self) -> None:
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

    def append(self, obj: DrawingObject) -> None:
        """Append a drawing object to the context.

        :param obj: The drawing object to add to the context.
        """
        self.drawing_objects.append(obj)
        self.redraw()

    def insert(self, index: int, obj: DrawingObject) -> None:
        """Insert a drawing object into the context at a specific index.

        :param index: The index at which the drawing object should be inserted.
        :param obj: The drawing object to add to the context.
        """
        self.drawing_objects.insert(index, obj)
        self.redraw()

    def remove(self, obj: DrawingObject) -> None:
        """Remove a drawing object from the context.

        :param obj: The drawing object to remove.
        """
        self.drawing_objects.remove(obj)
        self.redraw()

    def clear(self) -> None:
        """Remove all drawing objects from the context."""
        self.drawing_objects.clear()
        self.redraw()

    ###########################################################################
    # Path manipulation
    ###########################################################################

    def begin_path(self) -> BeginPath:
        """Start a new path in the canvas context.

        :returns: The ``BeginPath`` :any:`DrawingObject` for the operation.
        """
        begin_path = BeginPath()
        self.append(begin_path)
        return begin_path

    def close_path(self) -> ClosePath:
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

    def move_to(self, x: float, y: float) -> MoveTo:
        """Moves the current point of the canvas context without drawing.

        :param x: The x coordinate of the new current point.
        :param y: The y coordinate of the new current point.
        :returns: The ``MoveTo`` :any:`DrawingObject` for the operation.
        """
        move_to = MoveTo(x, y)
        self.append(move_to)
        return move_to

    def line_to(self, x: float, y: float) -> LineTo:
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
    ) -> BezierCurveTo:
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

    def quadratic_curve_to(
        self,
        cpx: float,
        cpy: float,
        x: float,
        y: float,
    ) -> QuadraticCurveTo:
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
    ) -> Arc:
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
    ) -> Ellipse:
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

    def rect(self, x: float, y: float, width: float, height: float) -> Rect:
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
    ) -> Fill:
        """Fill the current path.

        The fill can use either the `Non-Zero
        <https://en.wikipedia.org/wiki/Nonzero-rule>`__ or `Even-Odd
        <https://en.wikipedia.org/wiki/Even-odd_rule>`__ winding rule for filling paths.

        :param fill_rule: `nonzero` is the non-zero winding rule; `evenodd` is the
            even-odd winding rule.
        :param color: The fill color.
        :returns: The ``Fill`` :any:`DrawingObject` for the operation.
        """
        fill = Fill(color, fill_rule)
        self.append(fill)
        return fill

    def stroke(
        self,
        color: str = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ) -> Stroke:
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
        line_height_factor: float = 1,
    ) -> WriteText:
        """Write text at a given position in the canvas context.

        Drawing text is effectively a series of path operations, so the text will have
        the color and fill properties of the canvas context.

        :param text: The text to draw. Newlines will cause line breaks, but long lines
            will not be wrapped.
        :param x: The X coordinate of the text's left edge.
        :param y: The Y coordinate: its meaning depends on ``baseline``.
        :param font: The font in which to draw the text. The default is the system font.
        :param baseline: Alignment of text relative to the Y coordinate.
        :param line_height_factor: Height of the line box as a multiple of the font size
            when multiple lines are present.
        :returns: The ``WriteText`` :any:`DrawingObject` for the operation.
        """
        write_text = WriteText(text, x, y, font, baseline, line_height_factor)
        self.append(write_text)
        return write_text

    ###########################################################################
    # Transformations
    ###########################################################################
    def rotate(self, radians: float) -> Rotate:
        """Add a rotation to the canvas context.

        :param radians: The angle to rotate clockwise in radians.
        :returns: The ``Rotate`` :any:`DrawingObject` for the transformation.
        """
        rotate = Rotate(radians)
        self.append(rotate)
        return rotate

    def scale(self, sx: float, sy: float) -> Scale:
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

    def translate(self, tx: float, ty: float) -> Translate:
        """Add a translation to the canvas context.

        :param tx: Translation for the X dimension.
        :param ty: Translation for the Y dimension.
        :returns: The ``Translate`` :any:`DrawingObject` for the transformation.
        """
        translate = Translate(tx, ty)
        self.append(translate)
        return translate

    def reset_transform(self) -> ResetTransform:
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
    def Context(self) -> Iterator[Context]:
        """Construct and yield a new sub-:class:`~toga.widgets.canvas.Context` within
        this context.

        :yields: The new :class:`~toga.widgets.canvas.Context` object.
        """
        context = Context(canvas=self._canvas)
        self.append(context)
        yield context
        self.redraw()

    @contextmanager
    def ClosedPath(
        self,
        x: float | None = None,
        y: float | None = None,
    ) -> Iterator[ClosedPathContext]:
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
    ) -> Iterator[FillContext]:
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
    ) -> Iterator[StrokeContext]:
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl: Any, **kwargs: Any) -> None:
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

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"color={self.color!r}, fill_rule={self.fill_rule})"
        )

    def _draw(self, impl: Any, **kwargs: Any) -> None:
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
    def color(self, value: Color | str | None) -> None:
        if value is None:
            self._color = parse_color(BLACK)
        else:
            self._color = parse_color(value)


class StrokeContext(ClosedPathContext):
    """Construct a drawing context that will draw a stroke on all paths defined
    within the context.

    This is a context manager; it creates a new path, and moves to the start coordinate;
    when the context exits, the path is drawn with the stroke. For fine-grained control
    of a path, you can use :class:`~toga.widgets.canvas.Context.begin_path`,
    :class:`~toga.widgets.canvas.Context.move_to`,
    :class:`~toga.widgets.canvas.Context.close_path` and
    :class:`~toga.widgets.canvas.Context.stroke`.

    If both an x and y coordinate is provided, the drawing context will begin with
    a ``move_to`` operation in that context.

    You should not create a :class:`~toga.widgets.canvas.StrokeContext` context
    directly; instead, you should use the :meth:`~toga.widgets.canvas.Context.Stroke`
    method on an existing context.
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

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, color={self.color!r}, "
            f"line_width={self.line_width}, line_dash={self.line_dash!r})"
        )

    def _draw(self, impl: Any, **kwargs: Any) -> None:
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
    def color(self, value: object) -> None:
        if value is None:
            self._color = parse_color(BLACK)
        else:
            self._color = parse_color(value)
