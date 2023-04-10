import warnings
from contextlib import contextmanager
from enum import Enum
from math import pi

from toga.colors import BLACK, color as parse_color
from toga.fonts import SYSTEM, Font
from toga.handlers import wrapped_handler

from .. import Image
from .base import Widget


class FillRule(Enum):
    EVENODD = 0
    NONZERO = 1


class Context:
    """The user-created :class:`Context` drawing object to populate a drawing
    with visual context.

    The top left corner of the canvas must be painted at the origin of
    the context and is sized using the rehint() method.
    """

    def __init__(self, *args, **kwargs):  # kwargs used to support multiple inheritance
        super().__init__(*args, **kwargs)
        self._canvas = None
        self.drawing_objects = []

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def _draw(self, impl, *args, **kwargs):
        """Draw all drawing objects that are on the context or canvas.

        This method is used by the implementation to tell the interface
        canvas to draw all objects on it, and used by a context to draw
        all the objects that are on the context.
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
        """A drawing object to add to the drawing object stack on a context.

        Args:
            draw_obj: (:obj:`Drawing Object`): The drawing object to add
        """
        self.drawing_objects.append(draw_obj)

        # Only redraw if drawing to canvas directly
        if self.canvas is self:
            self.redraw()

        return draw_obj

    def redraw(self):
        """Force a redraw of the Canvas.

        The Canvas will be automatically redrawn after adding or remove
        a drawing object. If you modify a drawing object, this method is
        used to force a redraw.
        """
        self.canvas._impl.redraw()

    ###########################################################################
    # Operations on drawing objects
    ###########################################################################

    def remove(self, drawing_object):
        """Remove a drawing object.

        Args:
            drawing_object (:obj:'Drawing Object'): The drawing object to remove
        """
        self.drawing_objects.remove(drawing_object)
        self.redraw()

    def clear(self):
        """Remove all drawing objects."""
        self.drawing_objects.clear()
        self.redraw()

    ###########################################################################
    # Contexts to draw with
    ###########################################################################

    @contextmanager
    def context(self):
        """Constructs and returns a :class:`Context`.

        Makes use of an existing context. The top left corner of the canvas must
        be painted at the origin of the context and is sized using the rehint()
        method.

        Yields:
            :class:`Context` object.
        """
        context = Context()
        self.add_draw_obj(context)
        context.canvas = self.canvas
        yield context
        self.redraw()

    @contextmanager
    def fill(self, color=BLACK, fill_rule=FillRule.NONZERO, preserve=False):
        """Constructs and yields a :class:`Fill`.

        A drawing operator that fills the current path according to the current
        fill rule, (each sub-path is implicitly closed before being filled).

        Args:
            fill_rule (str, Optional): 'nonzero' is the non-zero winding rule and
                                       'evenodd' is the even-odd winding rule.
            preserve (bool, Optional): Preserves the path within the Context.
            color (str, Optional): color value in any valid color format,
                default to black.

        Yields:
            :class:`Fill` object.
        """
        fill = Fill(color, fill_rule, preserve)
        fill.canvas = self.canvas
        yield self.add_draw_obj(fill)
        self.redraw()

    @contextmanager
    def stroke(self, color=BLACK, line_width=2.0, line_dash=None):
        """Constructs and yields a :class:`Stroke`.

        Args:
            color (str, Optional): color value in any valid color format,
                default to black.
            line_width (float, Optional): stroke line width, default is 2.0.
            line_dash (array of floats, Optional): stroke line dash pattern, default is None.

        Yields:
            :class:`Stroke` object.
        """
        stroke = Stroke(color, line_width, line_dash)
        stroke.canvas = self.canvas
        yield self.add_draw_obj(stroke)
        self.redraw()

    @contextmanager
    def closed_path(self, x, y):
        """Calls move_to(x,y) and then constructs and yields a
        :class:`ClosedPath`.

        Args:
            x (float): The x axis of the beginning point.
            y (float): The y axis of the beginning point.

        Yields:
            :class:`ClosedPath` object.

        """
        closed_path = ClosedPath(x, y)
        closed_path.canvas = self.canvas
        yield self.add_draw_obj(closed_path)
        self.redraw()

    ###########################################################################
    # Paths to draw with
    ###########################################################################

    def new_path(self):
        """Constructs and returns a :class:`NewPath`.

        Returns:
            :class: `NewPath` object.
        """
        new_path = NewPath()
        return self.add_draw_obj(new_path)

    def move_to(self, x, y):
        """Constructs and returns a :class:`MoveTo`.

        Args:
            x (float): The x axis of the point.
            y (float): The y axis of the point.

        Returns:
            :class:`MoveTo` object.
        """
        move_to = MoveTo(x, y)
        return self.add_draw_obj(move_to)

    def line_to(self, x, y):
        """Constructs and returns a :class:`LineTo`.

        Args:
            x (float): The x axis of the coordinate for the end of the line.
            y (float): The y axis of the coordinate for the end of the line.

        Returns:
            :class:`LineTo` object.
        """
        line_to = LineTo(x, y)
        return self.add_draw_obj(line_to)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        """Constructs and returns a :class:`BezierCurveTo`.

        Args:
            cp1x (float): x coordinate for the first control point.
            cp1y (float): y coordinate for first control point.
            cp2x (float): x coordinate for the second control point.
            cp2y (float): y coordinate for the second control point.
            x (float): x coordinate for the end point.
            y (float): y coordinate for the end point.

        Returns:
            :class:`BezierCurveTo` object.
        """
        bezier_curve_to = BezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)
        return self.add_draw_obj(bezier_curve_to)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        """Constructs and returns a :class:`QuadraticCurveTo`.

        Args:
            cpx (float): The x axis of the coordinate for the control point.
            cpy (float): The y axis of the coordinate for the control point.
            x (float): The x axis of the coordinate for the end point.
            y (float): The y axis of the coordinate for the end point.

        Returns:
            :class:`QuadraticCurveTo` object.
        """
        quadratic_curve_to = QuadraticCurveTo(cpx, cpy, x, y)
        return self.add_draw_obj(quadratic_curve_to)

    def arc(self, x, y, radius, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        """Constructs and returns a :class:`Arc`.

        :param x: The x coordinate of the arc's center.
        :param y: The y coordinate of the arc's center.
        :param radius: The arc's radius.
        :param startangle: The angle (in radians) at which the
                arc starts, measured clockwise from the positive x axis,
                default 0.0.
        :param endangle: The angle (in radians) at which the arc ends,
                measured clockwise from the positive x axis, default 2*pi.
        :param anticlockwise: If true, causes the arc to be drawn
                counter-clockwise between the two angles instead of clockwise,
                default false.

        :returns: :class:`Arc` object.
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
        """Constructs and returns a :class:`Ellipse`.

        :param x: The x axis of the coordinate for the ellipse's center.
        :param y: The y axis of the coordinate for the ellipse's center.
        :param radiusx: The ellipse's major-axis radius.
        :param radiusy: The ellipse's minor-axis radius.
        :param rotation: The rotation for this ellipse, expressed in radians,
            default 0.0.
        :param startangle: The starting point in radians, measured from the x
            axis, from which it will be drawn, default 0.0.
        :param endangle: The end ellipse's angle in radians to which it will e
            drawn, default 2*pi.
        :param anticlockwise: If true, draws the ellipse anticlockwise
            (counter-clockwise) instead of clockwise, default false.

        Returns:
            :class:`Ellipse` object.
        """
        ellipse = Ellipse(
            x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise
        )
        self.add_draw_obj(ellipse)
        return ellipse

    def rect(self, x, y, width, height):
        """Constructs and returns a :class:`Rect`.

        Args:
            x (float): x coordinate for the rectangle starting point.
            y (float): y coordinate for the rectangle starting point.
            width (float): The rectangle's width.
            height (float): The rectangle's width.

        Returns:
            :class:`Rect` object.
        """
        rect = Rect(x, y, width, height)
        return self.add_draw_obj(rect)

    ###########################################################################
    # Text drawing
    ###########################################################################

    def write_text(self, text, x=0, y=0, font=None):
        """Constructs and returns a :class:`WriteText`.

        Writes a given text at the given (x,y) position. If no font is provided,
        then it will use the font assigned to the Canvas Widget, if it exists,
        or use the default font if there is no font assigned.

        Args:
            text (str): The text to fill.
            x (float, Optional): The x coordinate of the text. Default to 0.
            y (float, Optional): The y coordinate of the text. Default to 0.
            font (:class:`~toga.fonts.Font`, Optional): The font to write with.

        Returns:
            :class:`WriteText` object.
        """
        if font is None:
            font = Font(family=SYSTEM, size=self._canvas.style.font_size)
        write_text = WriteText(text, x, y, font)
        return self.add_draw_obj(write_text)


class Fill(Context):
    """A user-created :class:`Fill` drawing object for a fill context.

    A drawing object that fills the current path according to the current
    fill rule, (each sub-path is implicitly closed before being filled).

    Args:
        color (str, Optional): Color value in any valid color format,
            default to black.
        fill_rule (str, Optional): 'nonzero' if the non-zero winding rule and
                                   'evenodd' if the even-odd winding rule.
        preserve (bool, Optional): Preserves the path within the Context.
    """

    def __init__(self, color=BLACK, fill_rule=FillRule.NONZERO, preserve=False):
        super().__init__()
        self.color = color
        self.fill_rule = fill_rule
        self.preserve = preserve

    def __repr__(self):
        return "{}(color={}, fill_rule={}, preserve={})".format(
            self.__class__.__name__, self.color, self.fill_rule, self.preserve
        )

    def _draw(self, impl, *args, **kwargs):
        """Used by parent to draw all objects that are part of the context."""
        impl.new_path(*args, **kwargs)
        for obj in self.drawing_objects:
            kwargs["fill_color"] = self.color
            obj._draw(impl, *args, **kwargs)
        impl.fill(self.color, self.fill_rule, self.preserve, *args, **kwargs)

    @property
    def fill_rule(self):
        return self._fill_rule

    @fill_rule.setter
    def fill_rule(self, fill_rule):
        if isinstance(fill_rule, str):
            try:
                fill_rule = FillRule[fill_rule.upper()]
            except KeyError:
                raise ValueError(
                    "fill rule should be one of the followings: {}".format(
                        ", ".join([value.name.lower() for value in FillRule])
                    )
                )
        self._fill_rule = fill_rule

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
    """A user-created :class:`Stroke` drawing object for a stroke context.

    A drawing operator that strokes the current path according to the
    current line style settings.

    Args:
        color (str, Optional): Color value in any valid color format,
            default to black.
        line_width (float, Optional): Stroke line width, default is 2.0.
        line_dash (array of floats, Optional): Stroke line dash pattern, default is None.
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
        """Used by parent to draw all objects that are part of the context."""
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
    """A user-created :class:`ClosedPath` drawing object for a closed path
    context.

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
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl, *args, **kwargs):
        """Used by parent to draw all objects that are part of the context."""
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
        on_resize (:obj:`Callable`): Handler to invoke when the canvas is resized.
        on_press (:obj:`Callable`): Handler to invoke when the primary
            (usually the left) button is pressed.
        on_release (:obj:`Callable`): Handler to invoke when the primary
            (usually the left) button is released.
        on_drag (:obj:`Callable`): Handler to invoke when cursor is dragged with
            the primary (usually the left) button pressed.
        on_alt_press (:obj:`Callable`): Handler to invoke when the alternate
            (usually the right) button pressed.
        on_alt_release (:obj:`Callable`): Handler to invoke when the alternate
            (usually the right) button released
        on_alt_drag (:obj:`Callable`): Handler to invoke when the cursor is
            dragged with the alternate (usually the right) button pressed.
    """

    def __init__(
        self,
        id=None,
        style=None,
        on_resize=None,
        on_press=None,
        on_release=None,
        on_drag=None,
        on_alt_press=None,
        on_alt_release=None,
        on_alt_drag=None,
        factory=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style)
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self._canvas = self

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
    def on_resize(self):
        """The handler to invoke when the canvas is resized.

        Returns:
            The handler that is invoked on canvas resize.
        """
        return self._on_resize

    @on_resize.setter
    def on_resize(self, handler):
        """Set the handler to invoke when the canvas is resized.

        Args:
            handler (:obj:`Callable`): The handler to invoke when the canvas is resized.
        """
        self._on_resize = wrapped_handler(self, handler)
        self._impl.set_on_resize(self._on_resize)

    @property
    def on_press(self):
        """Return the handler invoked when the primary (usually the left) mouse
        button is pressed.

        Returns:
            The handler that is invoked when the primary mouse button is pressed.
        """
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        """Set the handler to invoke when the primary (usually the left) mouse
        button is pressed.

        Args:
            handler (:obj:`Callable`): The handler to invoke when the
            primary mouse button is pressed.
        """
        self._on_press = wrapped_handler(self, handler)
        self._impl.set_on_press(self._on_press)

    @property
    def on_release(self):
        """Return the handler invoked when the primary (usually the left) mouse
        button is released.

        Returns:
            The handler that is invoked when the primary mouse button is released.
        """
        return self._on_release

    @on_release.setter
    def on_release(self, handler):
        """Set the handler to invoke when the primary (usually the left) mouse
        button is released.

        Args:
            handler (:obj:`Callable`): The handler to invoke when the
            primary mouse button is released.
        """
        self._on_release = wrapped_handler(self, handler)
        self._impl.set_on_release(self._on_release)

    @property
    def on_drag(self):
        """Return the handler invoked when the mouse is dragged with the
        primary (usually the left) mouse button is pressed.

        Returns:
            The handler that is invoked when the mouse is dragged with
            the primary button pressed.
        """
        return self._on_drag

    @on_drag.setter
    def on_drag(self, handler):
        """Set the handler to invoke when the mouse button is dragged with the
        primary (usually the left) button pressed.

        Args:
            handler (:obj:`Callable`): The handler to invoke when the
            mouse is dragged with the primary button pressed.
        """
        self._on_drag = wrapped_handler(self, handler)
        self._impl.set_on_drag(self._on_drag)

    @property
    def on_alt_press(self):
        """Return the handler to invoke when the alternate (usually the right)
        mouse button is pressed.

        Returns:
            The handler that is invoked when the alternate mouse button is pressed.
        """
        return self._on_alt_press

    @on_alt_press.setter
    def on_alt_press(self, handler):
        """Set the handler to invoke when the alternate (usually the right)
        mouse button is pressed.

        Args:
            handler (:obj:`Callable`): The handler to invoke when the
            alternate mouse button is pressed.
        """
        self._on_alt_press = wrapped_handler(self, handler)
        self._impl.set_on_alt_press(self._on_alt_press)

    @property
    def on_alt_release(self):
        """Return the handler to invoke when the alternate (usually the right)
        mouse button is released.

        Returns:
            The handler that is invoked when the alternate mouse button is released.
        """
        return self._on_alt_release

    @on_alt_release.setter
    def on_alt_release(self, handler):
        """Set the handler to invoke when the alternate (usually the right)
        mouse button is released.

        Args:
            handler (:obj:`Callable`): The handler to invoke when the
            alternate mouse button is released.
        """
        self._on_alt_release = wrapped_handler(self, handler)
        self._impl.set_on_alt_release(self._on_alt_release)

    @property
    def on_alt_drag(self):
        """Return the handler to invoke when the mouse is dragged while the
        alternate (usually the right) mouse button is pressed.

        Returns:
            The handler that is invoked when the mouse is dragged with
            the alternate mouse button pressed.
        """
        return self._on_alt_drag

    @on_alt_drag.setter
    def on_alt_drag(self, handler):
        """Set the handler to invoke when the mouse is dragged with the
        alternate (usually the right) button pressed.

        Args:
            handler (:obj:`Callable`): The handler to invoke when the
            mouse is dragged with the alternate button pressed.
        """
        self._on_alt_drag = wrapped_handler(self, handler)
        self._impl.set_on_alt_drag(self._on_alt_drag)

    ###########################################################################
    # Transformations of a canvas
    ###########################################################################

    def rotate(self, radians):
        """Constructs and returns a :class:`Rotate`.

        Args:
            radians (float): The angle to rotate clockwise in radians.

        Returns:
            :class:`Rotate` object.
        """
        rotate = Rotate(radians)
        return self.add_draw_obj(rotate)

    def scale(self, sx, sy):
        """Constructs and returns a :class:`Scale`.

        Args:
            sx (float): scale factor for the X dimension.
            sy (float): scale factor for the Y dimension.

        Returns:
            :class:`Scale` object.
        """
        scale = Scale(sx, sy)
        return self.add_draw_obj(scale)

    def translate(self, tx, ty):
        """Constructs and returns a :class:`Translate`.

        Args:
            tx (float): X value of coordinate.
            ty (float): Y value of coordinate.

        Returns:
            :class:`Translate` object.
        """
        translate = Translate(tx, ty)
        return self.add_draw_obj(translate)

    def reset_transform(self):
        """Constructs and returns a :class:`ResetTransform`.

        Returns:
            :class:`ResetTransform` object.
        """
        reset_transform = ResetTransform()
        return self.add_draw_obj(reset_transform)

    ###########################################################################
    # Text measurement
    ###########################################################################

    def measure_text(self, text, font, tight=False):
        return self._impl.measure_text(text, font, tight=tight)

    ###########################################################################
    # As image
    ###########################################################################

    def as_image(self):
        return Image(data=self._impl.get_image_data())


class MoveTo:
    """A user-created :class:`MoveTo` drawing object which moves the start of
    the next operation to a point.

    Moves the starting point of a new sub-path to the (x, y) coordinates.


    Args:
        x (float): The x axis of the point.
        y (float): The y axis of the point.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation."""
        impl.move_to(self.x, self.y, *args, **kwargs)


class LineTo:
    """A user-created :class:`LineTo` drawing object which draws a line to a
    point.

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
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation."""
        impl.line_to(self.x, self.y, *args, **kwargs)


class BezierCurveTo:
    """A user-created :class:`BezierCurveTo` drawing object which adds a Bézier
    curve.

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
        """Draw the drawing object using the implementation."""
        impl.bezier_curve_to(
            self.cp1x, self.cp1y, self.cp2x, self.cp2y, self.x, self.y, *args, **kwargs
        )


class QuadraticCurveTo:
    """A user-created :class:`QuadraticCurveTo` drawing object which adds a
    quadratic curve.

    It requires two points. The first point is a control point and the
    second one is the end point. The starting point is the last point in the
    current path, which can be changed using ``moveTo()`` before creating the
    quadratic Bézier curve.

    :param cpx: The x axis of the coordinate for the control point.
    :param cpy: The y axis of the coordinate for the control point.
    :param x: The x axis of the coordinate for the end point.
    :param y: he y axis of the coordinate for the end point.
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
        """Draw the drawing object using the implementation."""
        impl.quadratic_curve_to(self.cpx, self.cpy, self.x, self.y, *args, **kwargs)


class Ellipse:
    """A user-created :class:`Ellipse` drawing object which adds an ellipse.

    The ellipse is centered at ``(x, y)`` position with the radii ``radiusx``
    and ``radiusy`` starting at ``startangle`` and ending at ``endangle`` going
    in the given direction by anticlockwise (defaulting to clockwise).

    :param x: The x axis of the coordinate for the ellipse's center.
    :param y: The y axis of the coordinate for the ellipse's center.
    :param radiusx: The ellipse's major-axis radius.
    :param radiusy: The ellipse's minor-axis radius.
    :param rotation: The rotation for this ellipse, expressed in radians, default
        0.0.
    :param startangle: The starting point in radians, measured from the x axis,
        from which it will be drawn, default 0.0.
    :param endangle: The end ellipse's angle in radians to which it will be
        drawn, default 2*pi.
    :param anticlockwise: If true, draws the ellipse anticlockwise
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
        return (
            "{}(x={}, y={}, radiusx={}, radiusy={}, "
            "rotation={}, startangle={}, endangle={}, anticlockwise={})".format(
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
        )

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation."""
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
            **kwargs,
        )


class Arc:
    """A user-created :class:`Arc` drawing object which adds an arc.

    The arc is centered at ``(x, y)`` position with radius ``r`` starting at
    ``startangle`` and ending at ``endangle`` going in the given direction by
    anticlockwise (defaulting to clockwise).

    :param x: The x coordinate of the arc's center.
    :param y: The y coordinate of the arc's center.
    :param radius: The arc's radius.
    :param startangle: The angle (in radians) at which the arc starts, measured
        clockwise from the positive x axis, default 0.0.
    :param endangle: The angle (in radians) at which the arc ends, measured
        clockwise from the positive x axis, default 2*pi.
    :param anticlockwise: If true, causes the arc to be drawn counter-clockwise
        between the two angles instead of clockwise, default false.
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
        """Draw the drawing object using the implementation."""
        impl.arc(
            self.x,
            self.y,
            self.radius,
            self.startangle,
            self.endangle,
            self.anticlockwise,
            *args,
            **kwargs,
        )


class Rect:
    """A user-created :class:`Rect` drawing object which adds a rectangle.

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
        """Draw the drawing object using the implementation."""
        impl.rect(self.x, self.y, self.width, self.height, *args, **kwargs)


class Rotate:
    """A user-created :class:`Rotate` to add canvas rotation.

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
        return f"{self.__class__.__name__}(radians={self.radians})"

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation."""
        impl.rotate(self.radians, *args, **kwargs)


class Scale:
    """A user-created :class:`Scale` to add canvas scaling.

    Modifies the canvas by scaling the X and Y canvas axes by sx and sy.

    Args:
        sx (float): scale factor for the X dimension.
        sy (float): scale factor for the Y dimension.
    """

    def __init__(self, sx, sy):
        self.sx = sx
        self.sy = sy

    def __repr__(self):
        return f"{self.__class__.__name__}(sx={self.sx}, sy={self.sy})"

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation."""
        impl.scale(self.sx, self.sy, *args, **kwargs)


class Translate:
    """A user-created :class:`Translate` to translate the canvas.

    Modifies the canvas by translating the canvas origin by (tx, ty).

    Args:
        tx (float): X value of coordinate.
        ty (float): Y value of coordinate.
    """

    def __init__(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def __repr__(self):
        return f"{self.__class__.__name__}(tx={self.tx}, ty={self.ty})"

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation."""
        impl.translate(self.tx, self.ty, *args, **kwargs)


class ResetTransform:
    """A user-created :class:`ResetTransform` to reset the canvas.

    Resets the canvas by setting it equal to the canvas with no
    transformations.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation."""
        impl.reset_transform(*args, **kwargs)


class WriteText:
    """A user-created :class:`WriteText` to add text.

    Writes a given text at the given (x,y) position. If no font is provided,
    then it will use the font assigned to the Canvas Widget, if it exists,
    or use the default font if there is no font assigned.

    Args:
        text (str): The text to fill.
        x (float, Optional): The x coordinate of the text. Default to 0.
        y (float, Optional): The y coordinate of the text. Default to 0.
        font (:class:`toga.fonts.Font`, Optional): The font to write with.
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
        """Draw the drawing object using the implementation."""
        impl.write_text(self.text, self.x, self.y, self.font, *args, **kwargs)


class NewPath:
    """A user-created :class:`NewPath` to add a new path."""

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def _draw(self, impl, *args, **kwargs):
        """Draw the drawing object using the implementation."""
        impl.new_path(*args, **kwargs)
