from contextlib import contextmanager
from math import pi

from toga.colors import color as parse_color, BLACK
from toga.fonts import Font, SYSTEM
from toga.handlers import wrapped_handler

from .base import Widget


class Context:
    """The user-created :class:`Context <Context>` drawing object to populate a
    drawing with visual context.

    The top left corner of the canvas must be painted at the origin of the
    context and is sized using the rehint() method.

    """

    def __init__(self, *args, **kwargs):  # kwargs used to support multiple inheritance
        super().__init__(*args, **kwargs)
        self._canvas = None
        self.drawing_objects = []

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def _draw(self, impl, *args, **kwargs):
        """Draw all drawing objects that are on the context or canvas.


        This method is used by the implementation to tell the interface canvas
        to draw all objects on it, and used by a context to draw all the
        objects that are on the context.

        """
        for obj in self.drawing_objects:
            obj._draw(impl, *args, **kwargs)

    ###########################################################################
    # Methods to keep track of the canvas, automatically redraw it
    ###########################################################################

    @property
    def canvas(self):
        """The canvas property of the current context.

        Returns:
            The canvas node. Returns self if this node *is* the canvas node.

        """
        return self._canvas if self._canvas else self

    @canvas.setter
    def canvas(self, value):
        """Set the canvas of the context.

        Args:
            value: The canvas to set.

        """
        self._canvas = value

    def add_draw_obj(self, draw_obj):
        """A drawing object to add to the drawing object stack on a context

        Args:
            draw_obj: (:obj:`Drawing Object`): The drawing object to add

        """
        self.drawing_objects.append(draw_obj)

        # Only redraw if drawing to canvas directly
        if self.canvas is self:
            self.redraw()

        return draw_obj

    def redraw(self):
        """Force a redraw of the Canvas

        The Canvas will be automatically redrawn after adding or remove a
        drawing object. If you modify a drawing object, this method is used to
        force a redraw.

        """
        self.canvas._impl.redraw()

    ###########################################################################
    # Operations on drawing objects
    ###########################################################################

    def remove(self, drawing_object):
        """Remove a drawing object

        Args:
            drawing_object (:obj:'Drawing Object'): The drawing object to remove

        """
        self.drawing_objects.remove(drawing_object)
        self.redraw()

    def clear(self):
        """Remove all drawing objects
        """
        self.drawing_objects.clear()
        self.redraw()

    ###########################################################################
    # Contexts to draw with
    ###########################################################################

    @contextmanager
    def context(self):
        """Constructs and returns a :class:`Context <Context>`.

        Makes use of an existing context. The top left corner of the canvas must
        be painted at the origin of the context and is sized using the rehint()
        method.

        Yields:
            :class:`Context <Context>` object.

        """
        context = Context()
        self.add_draw_obj(context)
        context.canvas = self.canvas
        yield context
        self.redraw()

    @contextmanager
    def fill(self, color=BLACK, fill_rule="nonzero", preserve=False):
        """Constructs and yields a :class:`Fill <Fill>`.

        A drawing operator that fills the current path according to the current
        fill rule, (each sub-path is implicitly closed before being filled).

        Args:
            fill_rule (str, optional): 'nonzero' is the non-zero winding rule and
                                       'evenodd' is the even-odd winding rule.
            preserve (bool, optional): Preserves the path within the Context.
            color (str, optional): color value in any valid color format,
                default to black.

        Yields:
            :class:`Fill <Fill>` object.

        """
        if fill_rule is "evenodd":
            fill = Fill(color, fill_rule, preserve)
        else:
            fill = Fill(color, "nonzero", preserve)
        fill.canvas = self.canvas
        yield self.add_draw_obj(fill)
        self.redraw()

    @contextmanager
    def stroke(self, color=BLACK, line_width=2.0, line_dash=None):
        """Constructs and yields a :class:`Stroke <Stroke>`.

        Args:
            color (str, optional): color value in any valid color format,
                default to black.
            line_width (float, optional): stroke line width, default is 2.0.
            line_dash (array of floats, optional): stroke line dash pattern, default is None.

        Yields:
            :class:`Stroke <Stroke>` object.

        """
        stroke = Stroke(color, line_width, line_dash)
        stroke.canvas = self.canvas
        yield self.add_draw_obj(stroke)
        self.redraw()

    @contextmanager
    def closed_path(self, x, y):
        """Calls move_to(x,y) and then constructs and yields a
        :class:`ClosedPath <ClosedPath>`.

        Args:
            x (float): The x axis of the beginning point.
            y (float): The y axis of the beginning point.

        Yields:
            :class:`ClosedPath <ClosedPath>` object.

        """
        closed_path = ClosedPath(x, y)
        closed_path.canvas = self.canvas
        yield self.add_draw_obj(closed_path)
        self.redraw()

    ###########################################################################
    # Paths to draw with
    ###########################################################################

    def new_path(self):
        """Constructs and returns a :class:`NewPath <NewPath>`.

        Returns:
            :class: `NewPath <NewPath>` object.

        """
        new_path = NewPath()
        return self.add_draw_obj(new_path)

    def move_to(self, x, y):
        """Constructs and returns a :class:`MoveTo <MoveTo>`.

        Args:
            x (float): The x axis of the point.
            y (float): The y axis of the point.

        Returns:
            :class:`MoveTo <MoveTo>` object.

        """
        move_to = MoveTo(x, y)
        return self.add_draw_obj(move_to)

    def line_to(self, x, y):
        """Constructs and returns a :class:`LineTo <LineTo>`.

        Args:
            x (float): The x axis of the coordinate for the end of the line.
            y (float): The y axis of the coordinate for the end of the line.

        Returns:
            :class:`LineTo <LineTo>` object.

        """
        line_to = LineTo(x, y)
        return self.add_draw_obj(line_to)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        """Constructs and returns a :class:`BezierCurveTo <BezierCurveTo>`.

        Args:
            cp1x (float): x coordinate for the first control point.
            cp1y (float): y coordinate for first control point.
            cp2x (float): x coordinate for the second control point.
            cp2y (float): y coordinate for the second control point.
            x (float): x coordinate for the end point.
            y (float): y coordinate for the end point.

        Returns:
            :class:`BezierCurveTo <BezierCurveTo>` object.

        """
        bezier_curve_to = BezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)
        return self.add_draw_obj(bezier_curve_to)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        """Constructs and returns a :class:`QuadraticCurveTo <QuadraticCurveTo>`.

        Args:
            cpx (float): The x axis of the coordinate for the control point.
            cpy (float): The y axis of the coordinate for the control point.
            x (float): The x axis of the coordinate for the end point.
            y (float): The y axis of the coordinate for the end point.

        Returns:
            :class:`QuadraticCurveTo <QuadraticCurveTo>` object.

        """
        quadratic_curve_to = QuadraticCurveTo(cpx, cpy, x, y)
        return self.add_draw_obj(quadratic_curve_to)

    def arc(self, x, y, radius, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        """Constructs and returns a :class:`Arc <Arc>`.

        Args:
            x (float): The x coordinate of the arc's center.
            y (float): The y coordinate of the arc's center.
            radius (float): The arc's radius.
            startangle (float, optional): The angle (in radians) at which the
                arc starts, measured clockwise from the positive x axis,
                default 0.0.
            endangle (float, optional): The angle (in radians) at which the arc ends,
                measured clockwise from the positive x axis, default 2*pi.
            anticlockwise (bool, optional): If true, causes the arc to be drawn
                counter-clockwise between the two angles instead of clockwise,
                default false.

        Returns:
            :class:`Arc <Arc>` object.

        """
        arc = Arc(x, y, radius, startangle, endangle, anticlockwise)
        return self.add_draw_obj(arc)

    def ellipse(
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
        """Constructs and returns a :class:`Ellipse <Ellipse>`.

        Args:
            x (float): The x axis of the coordinate for the ellipse's center.
            y (float): The y axis of the coordinate for the ellipse's center.
            radiusx (float): The ellipse's major-axis radius.
            radiusy (float): The ellipse's minor-axis radius.
            rotation (float, optional): The rotation for this ellipse, expressed in radians, default 0.0.
            startangle (float, optional): The starting point in radians, measured from the x
                axis, from which it will be drawn, default 0.0.
            endangle (float, optional): The end ellipse's angle in radians to which it will
                be drawn, default 2*pi.
            anticlockwise (bool, optional): If true, draws the ellipse
                anticlockwise (counter-clockwise) instead of clockwise, default false.

        Returns:
            :class:`Ellipse <Ellipse>` object.

        """
        ellipse = Ellipse(
            x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise
        )
        self.add_draw_obj(ellipse)
        return ellipse

    def rect(self, x, y, width, height):
        """Constructs and returns a :class:`Rect <Rect>`.

        Args:
            x (float): x coordinate for the rectangle starting point.
            y (float): y coordinate for the rectangle starting point.
            width (float): The rectangle's width.
            height (float): The rectangle's width.

        Returns:
            :class:`Rect <Rect>` object.

        """
        rect = Rect(x, y, width, height)
        return self.add_draw_obj(rect)

    ###########################################################################
    # Text drawing
    ###########################################################################

    def write_text(self, text, x=0, y=0, font=None):
        """Constructs and returns a :class:`WriteText <WriteText>`.

        Writes a given text at the given (x,y) position. If no font is provided,
        then it will use the font assigned to the Canvas Widget, if it exists,
        or use the default font if there is no font assigned.

        Args:
            text (string): The text to fill.
            x (float, optional): The x coordinate of the text. Default to 0.
            y (float, optional): The y coordinate of the text. Default to 0.
            font (:class:`toga.Font`, optional): The font to write with.

        Returns:
            :class:`WriteText <WriteText>` object.

        """
        if font is None:
            font = Font(family=SYSTEM, size=self._canvas.style.font_size)
        write_text = WriteText(text, x, y, font)
        return self.add_draw_obj(write_text)


class Fill(Context):
    """A user-created :class:`Fill <Fill>` drawing object for a fill context.

    A drawing object that fills the current path according to the current
    fill rule, (each sub-path is implicitly closed before being filled).

    Args:
        color (str, optional): Color value in any valid color format,
            default to black.
        fill_rule (str, optional): 'nonzero' if the non-zero winding rule and
                                   'evenodd' if the even-odd winding rule.
        preserve (bool, optional): Preserves the path within the Context.

    """

    def __init__(self, color=BLACK, fill_rule="nonzero", preserve=False):
        super().__init__()
        self.color = color
        self.fill_rule = fill_rule
        self.preserve = preserve

    def __repr__(self):
        return "{}(color={}, fill_rule={}, preserve={})".format(
            self.__class__.__name__, self.color, self.fill_rule, self.preserve
        )

    def _draw(self, impl, *args, **kwargs):
        """Used by parent to draw all objects that are part of the context.

        """
        impl.new_path(*args, **kwargs)
        for obj in self.drawing_objects:
            kwargs["fill_color"] = self.color
            obj._draw(impl, *args, **kwargs)
        impl.fill(self.color, self.fill_rule, self.preserve, *args, **kwargs)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value is None:
            self._color = None
        else:
            self._color = parse_color(value)


class Stroke(Context):
    """A user-created :class:`Stroke <Stroke>` drawing object for a stroke context.

    A drawing operator that strokes the current path according to the
    current line style settings.

    Args:
        color (str, optional): Color value in any valid color format,
            default to black.
        line_width (float, optional): Stroke line width, default is 2.0.
        line_dash (array of floats, optional): Stroke line dash pattern, default is None.

    """

    def __init__(self, color=BLACK, line_width=2.0, line_dash=None):
        super().__init__()
        self._color = None
        self.color = color
        self.line_width = line_width
        self.line_dash = line_dash

    def __repr__(self):
        return "{}(color={}, line_width={}, line_dash={})".format(
            self.__class__.__name__, self.color, self.line_width, self.line_dash
        )

    def _draw(self, impl, *args, **kwargs):
        """Used by parent to draw all objects that are part of the context.

        """
        for obj in self.drawing_objects:
            kwargs["stroke_color"] = self.color
            kwargs["text_line_width"] = self.line_width
            kwargs["text_line_dash"] = self.line_dash
            obj._draw(impl, *args, **kwargs)
        impl.stroke(self.color, self.line_width, self.line_dash, *args, **kwargs)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value is None:
            self._color = None
        else:
            self._color = parse_color(value)


class ClosedPath(Context):
    """A user-created :class:`ClosedPath <ClosedPath>` drawing object for a
    closed path context.

    Creates a new path and then closes it.

    Args:
        x (float): The x axis of the beginning point.
        y (float): The y axis of the beginning point.

    """

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}(x={}, y={})".format(self.__class__.__name__, self.x, self.y)

    def _draw(self, impl, *args, **kwargs):
        """Used by parent to draw all objects that are part of the context.

        """
        impl.move_to(self.x, self.y, *args, **kwargs)
        for obj in self.drawing_objects:
            obj._draw(impl, *args, **kwargs)
        impl.closed_path(self.x, self.y, *args, **kwargs)


class Canvas(Context, Widget):
    """Create new canvas.

    Args:
        id (str):  An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no
            style is provided then a new one will be created for the widget.
        on_resize (:obj:`callable`): Function to call when resized.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional &
            normally not needed)
    """

    def __init__(self, id=None, style=None, on_resize=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._canvas = self

        # Create a platform specific implementation of Canvas
        self._impl = self.factory.Canvas(interface=self)

        # Set all the properties
        self.on_resize = on_resize

    @property
    def on_resize(self):
        """The handler to invoke when the canvas is resized.

        Returns:
            The function ``callable`` that is called on canvas resize.
        """
        return self._on_resize

    @on_resize.setter
    def on_resize(self, handler):
        """Set the handler to invoke when the canvas is resized.

        Args:
            handler (:obj:`callable`): The handler to invoke when the canvas is resized.
        """
        self._on_resize = wrapped_handler(self, handler)
        self._impl.set_on_resize(self._on_resize)

    ###########################################################################
    # Transformations of a canvas
    ###########################################################################

    def rotate(self, radians):
        """Constructs and returns a :class:`Rotate <Rotate>`.

        Args:
            radians (float): The angle to rotate clockwise in radians.

        Returns:
            :class:`Rotate <Rotate>` object.

        """
        rotate = Rotate(radians)
        return self.add_draw_obj(rotate)

    def scale(self, sx, sy):
        """Constructs and returns a :class:`Scale <Scale>`.

        Args:
            sx (float): scale factor for the X dimension.
            sy (float): scale factor for the Y dimension.

        Returns:
            :class:`Scale <Scale>` object.

        """
        scale = Scale(sx, sy)
        return self.add_draw_obj(scale)

    def translate(self, tx, ty):
        """Constructs and returns a :class:`Translate <Translate>`.

        Args:
            tx (float): X value of coordinate.
            ty (float): Y value of coordinate.

        Returns:
            :class:`Translate <Translate>` object.

        """
        translate = Translate(tx, ty)
        return self.add_draw_obj(translate)

    def reset_transform(self):
        """Constructs and returns a :class:`ResetTransform <ResetTransform>`.

        Returns:
            :class:`ResetTransform <ResetTransform>` object.

        """
        reset_transform = ResetTransform()
        return self.add_draw_obj(reset_transform)


class MoveTo:
    """A user-created :class:`MoveTo <MoveTo>` drawing object which moves the
    start of the next operation to a point.

    Moves the starting point of a new sub-path to the (x, y) coordinates.


    Args:
        x (float): The x axis of the point.
        y (float): The y axis of the point.

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}(x={}, y={})".format(self.__class__.__name__, self.x, self.y)

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.move_to(self.x, self.y, *args, **kwargs)


class LineTo:
    """A user-created :class:`LineTo <LineTo>` drawing object which draws a line
    to a point.

    Connects the last point in the sub-path to the (x, y) coordinates
    with a straight line (but does not actually draw it).

    Args:
        x (float): The x axis of the coordinate for the end of the line.
        y (float): The y axis of the coordinate for the end of the line.

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}(x={}, y={})".format(self.__class__.__name__, self.x, self.y)

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.line_to(self.x, self.y, *args, **kwargs)


class BezierCurveTo:
    """A user-created :class:`BezierCurveTo <BezierCurveTo>` drawing
    object which adds a Bézier curve.

    It requires three points. The first two points are control points
    and the third one is the end point. The starting point is the last
    point in the current path, which can be changed using move_to() before
    creating the Bézier curve.

    Args:
        cp1x (float): x coordinate for the first control point.
        cp1y (float): y coordinate for first control point.
        cp2x (float): x coordinate for the second control point.
        cp2y (float): y coordinate for the second control point.
        x (float): x coordinate for the end point.
        y (float): y coordinate for the end point.

    """

    def __init__(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.cp1x = cp1x
        self.cp1y = cp1y
        self.cp2x = cp2x
        self.cp2y = cp2y
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}(cp1x={}, cp1y={}, cp2x={}, cp2y={}, x={}, y={})".format(
            self.__class__.__name__,
            self.cp1x,
            self.cp1y,
            self.cp2x,
            self.cp2y,
            self.x,
            self.y,
        )

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.bezier_curve_to(
            self.cp1x, self.cp1y, self.cp2x, self.cp2y, self.x, self.y, *args, **kwargs
        )


class QuadraticCurveTo:
    """A user-created :class:`QuadraticCurveTo <QuadraticCurveTo>` drawing
    object which adds a quadratic curve.

    It requires two points. The first point is a control point and the
    second one is the end point. The starting point is the last point in the
    current path, which can be changed using moveTo() before creating the
    quadratic Bézier curve.

    Args:
        cpx (float): The x axis of the coordinate for the control point.
        cpy (float): The y axis of the coordinate for the control point.
        x (float): The x axis of the coordinate for the end point.
        y (float): he y axis of the coordinate for the end point.

    """

    def __init__(self, cpx, cpy, x, y):
        self.cpx = cpx
        self.cpy = cpy
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}(cpx={}, cpy={}, x={}, y={})".format(
            self.__class__.__name__, self.cpx, self.cpy, self.x, self.y
        )

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.quadratic_curve_to(self.cpx, self.cpy, self.x, self.y, *args, **kwargs)


class Ellipse:
    """A user-created :class:`Ellipse <Ellipse>` drawing object which adds an ellipse.

    The ellipse is centered at (x, y) position with the radii radiusx and radiusy
    starting at startAngle and ending at endAngle going in the given
    direction by anticlockwise (defaulting to clockwise).

    Args:
        x (float): The x axis of the coordinate for the ellipse's center.
        y (float): The y axis of the coordinate for the ellipse's center.
        radiusx (float): The ellipse's major-axis radius.
        radiusy (float): The ellipse's minor-axis radius.
        rotation (float, optional): The rotation for this ellipse, expressed in radians, default 0.0.
        startangle (float, optional): The starting point in radians, measured from the x
            axis, from which it will be drawn, default 0.0.
        endangle (float, optional): The end ellipse's angle in radians to which it will
            be drawn, default 2*pi.
        anticlockwise (bool, optional): If true, draws the ellipse anticlockwise
            (counter-clockwise) instead of clockwise, default false.

    """

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
        self.x = x
        self.y = y
        self.radiusx = radiusx
        self.radiusy = radiusy
        self.rotation = rotation
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __repr__(self):
        return "{}(x={}, y={}, radiusx={}, radiusy={}, rotation={}, startangle={}, endangle={}, anticlockwise={})".format(
            self.__class__.__name__,
            self.x,
            self.y,
            self.radiusx,
            self.radiusy,
            self.rotation,
            self.startangle,
            self.endangle,
            self.anticlockwise,
        )

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.ellipse(
            self.x,
            self.y,
            self.radiusx,
            self.radiusy,
            self.rotation,
            self.startangle,
            self.endangle,
            self.anticlockwise,
            *args,
            **kwargs
        )


class Arc:
    """A user-created :class:`Arc <Arc>` drawing object which adds an arc.

    The arc is centered at (x, y) position with radius r starting at startangle
    and ending at endangle going in the given direction by anticlockwise
    (defaulting to clockwise).

    Args:
        x (float): The x coordinate of the arc's center.
        y (float): The y coordinate of the arc's center.
        radius (float): The arc's radius.
        startangle (float, optional): The angle (in radians) at which the
            arc starts, measured clockwise from the positive x axis,
            default 0.0.
        endangle (float, optional): The angle (in radians) at which the arc ends,
            measured clockwise from the positive x axis, default 2*pi.
        anticlockwise (bool, optional): If true, causes the arc to be drawn
            counter-clockwise between the two angles instead of clockwise,
            default false.

    """

    def __init__(
        self, x, y, radius, startangle=0.0, endangle=2 * pi, anticlockwise=False
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __repr__(self):
        return "{}(x={}, y={}, radius={}, startangle={}, endangle={}, anticlockwise={})".format(
            self.__class__.__name__,
            self.x,
            self.y,
            self.radius,
            self.startangle,
            self.endangle,
            self.anticlockwise,
        )

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.arc(
            self.x,
            self.y,
            self.radius,
            self.startangle,
            self.endangle,
            self.anticlockwise,
            *args,
            **kwargs
        )


class Rect:
    """A user-created :class:`Rect <Rect>` drawing object which adds a rectangle.

    The rectangle is at position (x, y) with a size that is determined by
    width and height. Those four points are connected by straight lines and
    the sub-path is marked as closed, so that you can fill or stroke this
    rectangle.

    Args:
        x (float): x coordinate for the rectangle starting point.
        y (float): y coordinate for the rectangle starting point.
        width (float): The rectangle's width.
        height (float): The rectangle's width.

    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return "{}(x={}, y={}, width={}, height={})".format(
            self.__class__.__name__, self.x, self.y, self.width, self.height
        )

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.rect(self.x, self.y, self.width, self.height, *args, **kwargs)


class Rotate:
    """A user-created :class:`Rotate <Rotate>` to add canvas rotation.

    Modifies the canvas by rotating the canvas by angle radians. The rotation
    center point is always the canvas origin which is in the upper left of the
    canvas. To change the center point, move the canvas by using the
    translate() method.

    Args:
        radians (float): The angle to rotate clockwise in radians.

    """

    def __init__(self, radians):
        self.radians = radians

    def __repr__(self):
        return "{}(radians={})".format(self.__class__.__name__, self.radians)

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.rotate(self.radians, *args, **kwargs)


class Scale:
    """A user-created :class:`Scale <Scale>` to add canvas scaling.

    Modifies the canvas by scaling the X and Y canvas axes by sx and sy.

    Args:
        sx (float): scale factor for the X dimension.
        sy (float): scale factor for the Y dimension.

    """

    def __init__(self, sx, sy):
        self.sx = sx
        self.sy = sy

    def __repr__(self):
        return "{}(sx={}, sy={})".format(self.__class__.__name__, self.sx, self.sy)

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.scale(self.sx, self.sy, *args, **kwargs)


class Translate:
    """A user-created :class:`Translate <Translate>` to translate the canvas.

    Modifies the canvas by translating the canvas origin by (tx, ty).

    Args:
        tx (float): X value of coordinate.
        ty (float): Y value of coordinate.

    """

    def __init__(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def __repr__(self):
        return "{}(tx={}, ty={})".format(self.__class__.__name__, self.tx, self.ty)

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.translate(self.tx, self.ty, *args, **kwargs)


class ResetTransform:
    """A user-created :class:`ResetTransform <ResetTransform>` to reset the
    canvas.

    Resets the canvas by setting it equal to the canvas with no
    transformations.

    """

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.reset_transform(*args, **kwargs)


class WriteText:
    """A user-created :class:`WriteText <WriteText>` to add text.

    Writes a given text at the given (x,y) position. If no font is provided,
    then it will use the font assigned to the Canvas Widget, if it exists,
    or use the default font if there is no font assigned.

    Args:
        text (string): The text to fill.
        x (float, optional): The x coordinate of the text. Default to 0.
        y (float, optional): The y coordinate of the text. Default to 0.
        font (:class:`toga.Font`, optional): The font to write with.

    """

    def __init__(self, text, x, y, font):
        self.text = text
        self.x = x
        self.y = y
        self.font = font

    def __repr__(self):
        return "{}(text={}, x={}, y={}, font={})".format(
            self.__class__.__name__, self.text, self.x, self.y, self.font
        )

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.write_text(self.text, self.x, self.y, self.font, *args, **kwargs)


class NewPath:
    """A user-created :class:`NewPath <NewPath>` to add a new path.

    """

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation.

        """
        impl.new_path(*args, **kwargs)
