from contextlib import contextmanager
from math import pi

from .base import Widget


class Canvas(Widget):
    """Create new canvas

    Args:
        id (str):  An identifier for this widget.
        style (:class:`colosseum.CSSNode`): An optional style object. If no
            style is provided then a new one will be created for the widget.
        on_draw (``callable``): Function to draw on the canvas.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional &
            normally not needed)
    """

    def __init__(self, id=None, style=None, on_draw=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of Canvas
        self._impl = self.factory.Canvas(interface=self)
        self.on_draw = on_draw

    def set_context(self, context):
        """The context of the Canvas to pass through from a callable function

        Args:
            context (:obj:'context'): The context to pass

        """
        self._impl.set_context(context)

    @property
    def on_draw(self):
        """The callable function to draw on a Canvas

        Creates a context or saves the current context, draws the operations
        using the passed function, then renders the drawing, and finally
        restores the saved context. The top left corner of the canvas must be
        painted at the origin of the context and is sized using the rehint()
        method.

        """
        return self._on_draw

    @on_draw.setter
    def on_draw(self, handler):
        self._on_draw = handler
        self._impl.set_on_draw(self._on_draw)

    # Line Styles

    def line_width(self, width=2.0):
        """Set width of lines

        Args:
            width (float): line width

        """
        self._impl.line_width(width)

    # Fill and Stroke Styles

    def fill_style(self, color=None):
        """Color to use inside shapes

        Currently supports color, in the future could support gradient and
        pattern. A named color or RGBA value must be passed, or default
        to black.
        Args:
            color (str): CSS color value or in rgba(0, 0, 0, 1) format

        """
        self._impl.fill_style(color)

    def stroke_style(self, color=None):
        """Color to use for lines around shapes

        Currently supports color, in the future could support gradient and
        pattern. A named color or RGBA value must be passed, or default to
        black. If using RGBA values, RGB are in the range 0-255, A is in the
        range 0-1.

        Args:
            color (str): CSS color value or in rgba(0, 0, 0, 1) format

        """
        self._impl.stroke_style(color)

    # Paths

    @contextmanager
    def closed_path(self, x, y):
        """Creates a new path and then closes it

        Yields: None

        """
        self._impl.move_to(x, y)
        yield
        self._impl.close_path()

    def move_to(self, x, y):
        """Moves the starting point of a new sub-path to the (x, y) coordinates.

        Args:
            x (float): The x axis of the point
            y (float): The y axis of the point

        """
        self._impl.move_to(x, y)

    def line_to(self, x, y):
        """Connects the last point with a line.

        Connects the last point in the sub-path to the (x, y) coordinates
        with a straight line (but does not actually draw it).

        Args:
            x (float): The x axis of the coordinate for the end of the line
            y (float): The y axis of the coordinate for the end of the line

        """
        self._impl.line_to(x, y)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        """Adds a cubic Bézier curve to the path.

        It requires three points. The first two points are control points
        and the third one is the end point. The starting point is the last
        point in the current path, which can be changed using move_to() before
        creating the Bézier curve.

        Args:
            cp1x (float): x coordinate for the first control point
            cp1y (float): y coordinate for first control point
            cp2x (float): x coordinate for the second control point
            cp2y (float): y coordinate for the second control point
            x (float): x coordinate for the end point
            y (float): y coordinate for the end point

        """
        self._impl.bezier_curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        """Adds a quadratic Bézier curve to the path.

        It requires two points. The first point is a control point and the
        second one is the end point. The starting point is the last point in the
        current path, which can be changed using moveTo() before creating the
        quadratic Bézier curve.

        Args:
            cpx (float): The x axis of the coordinate for the control point
            cpy (float): The y axis of the coordinate for the control point
            x (float): The x axis of the coordinate for the end point
            y (float): he y axis of the coordinate for the end point

        """
        self._impl.quadratic_curve_to(cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle=0, endangle=2 * pi, anticlockwise=False):
        """Adds an arc to the path.

        The arc is centered at (x, y) position with radius r starting at
        startAngle and ending at endAngle going in the given direction by
        anticlockwise (defaulting to clockwise).

        Args:
            x (float): The x coordinate of the arc's center
            y (float): The y coordinate of the arc's center
            radius (float): The arc's radius
            startangle (float): The angle (in radians) at which the arc starts,
                measured clockwise from the positive x axis
            endangle (float): The angle (in radians) at which the arc ends,
                measured clockwise from the positive x axis
            anticlockwise (bool): Optional, if true, causes the arc to be drawn
                counter-clockwise between the two angles instead of clockwise

        """
        self._impl.arc(x, y, radius, startangle, endangle, anticlockwise)

    def ellipse(self, x, y, radiusx, radiusy, rotation=0, startangle=0, endangle=2 * pi, anticlockwise=False):
        """Adds an ellipse to the path.

        The ellipse is centered at (x, y) position with the radii radiusx and radiusy
        starting at startAngle and ending at endAngle going in the given
        direction by anticlockwise (defaulting to clockwise).

        Args:
            x (float): The x axis of the coordinate for the ellipse's center
            y (float): The y axis of the coordinate for the ellipse's center
            radiusx (float): The ellipse's major-axis radius
            radiusy (float): The ellipse's minor-axis radius
            rotation (float): The rotation for this ellipse, expressed in radians
            startangle (float): The starting point in radians, measured from the x
                axis, from which it will be drawn
            endangle (float): The end ellipse's angle in radians to which it will
                be drawn
            anticlockwise (bool): Optional, if true, draws the ellipse
                anticlockwise (counter-clockwise) instead of clockwise

        """
        self._impl.ellipse(x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise)

    def rect(self, x, y, width, height):
        """ Creates a path for a rectangle.

        The rectangle is at position (x, y) with a size that is determined by
        width and height. Those four points are connected by straight lines and
        the sub-path is marked as closed, so that you can fill or stroke this
        rectangle.

        Args:
            x (float): x coordinate for the rectangle starting point
            y (float): y coordinate for the rectangle starting point
            width (float): The rectangle's width
            height (float): The rectangle's width

        """
        self._impl.rect(x, y, width, height)

    # Drawing Paths

    @contextmanager
    def fill(self, fill_rule='nonzero', preserve=False):
        """Fills the subpaths with the current fill style

        A drawing operator that fills the current path according to the current
        fill rule, (each sub-path is implicitly closed before being filled).

        Args:
            fill_rule (str): 'nonzero' is the non-zero winding rule and
                             'evenodd' is the even-odd winding rule
            preserve (bool): Preserves the path within the Context

        """
        self._impl.new_path()
        yield
        if fill_rule is 'evenodd':
            self._impl.fill(fill_rule, preserve)
        else:
            self._impl.fill('nonzero', preserve)

    @contextmanager
    def stroke(self):
        """Strokes the subpaths with the current stroke style

        A drawing operator that strokes the current path according to the
        current line style settings.

        """
        yield
        self._impl.stroke()

    # Transformations

    def rotate(self, radians):
        """Moves the transformation matrix by the angle

        Modifies the current transformation matrix (CTM) by rotating the
        user-space axes by angle radians. The rotation of the axes takes places
        after any existing transformation of user space. The rotation center
        point is always the canvas origin. To change the center point, move the
        canvas by using the translate() method.

        Args:
            radians (float): The angle to rotate clockwise in radians

        """
        self._impl.rotate(radians)

    def scale(self, sx, sy):
        """Adds a scaling transformation to the canvas

        Modifies the current transformation matrix (CTM) by scaling the X and Y
        user-space axes by sx and sy respectively. The scaling of the axes takes
        place after any existing transformation of user space.

        Args:
            sx (float): scale factor for the X dimension
            sy (float): scale factor for the Y dimension

        """
        self._impl.scale(sx, sy)

    def translate(self, tx, ty):
        """Moves the canvas and its origin

        Modifies the current transformation matrix (CTM) by translating the
        user-space origin by (tx, ty). This offset is interpreted as a
        user-space coordinate according to the CTM in place before the new call
        to translate(). In other words, the translation of the user-space origin
        takes place after any existing transformation.

        Args:
            tx (float): X value of coordinate
            ty (float): Y value of coordinate

        """
        self._impl.translate(tx, ty)

    def reset_transform(self):
        """Reset the current transform by the identity matrix

        Resets the current transformation Matrix (CTM) by setting it equal to
        the identity matrix. That is, the user-space and device-space axes will
        be aligned and one user-space unit will transform to one device-space
        unit.

        """
        self._impl.reset_transform()
