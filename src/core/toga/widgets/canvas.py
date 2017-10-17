from .base import Widget


class Canvas(Widget):
    """ Create new canvas

    Args:
        id (str):  An identifier for this widget.
        style (:class:`colosseum.CSSNode`): An optional style object. If no
            style is provided then a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional &
            normally not needed)
    """

    def __init__(self, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.Canvas(interface=self)

        self.rehint()

class Path2D(Widget):
    """Create paths which consist of straight and curved line segments joined.

    Args:
        id (str):  An identifier for this widget.
        style (:class:`colosseum.CSSNode`): An optional style object. If no
        style is provided then a new one will be created for the widget.
        path (:class:'toga.Path2D'): When optionally invoked with another Path2D
            object, a copy of the path argument is created.
        d (str): When invoked with a SVG path data, a new path is created from
            that description.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally
            not needed)

    """

    def __init__(self, id=None, style=None, path=None, d=None, factory=None):

        self._impl = self.factory.Path2D(interface=self)

        self.path = path
        self.d = d

        self.rehint()

    def add_path(self, path, transform):
        """Adds another path to the path.

        Args:
            path: A Path2D path to add
            transform: An optional SVGMatrix to be used as the transformation
                matrix for the path that is added
        """
        return self._impl.addPath(path, transform)

    def close_path(self):
        """Closes a path

         Causes the point of the pen to move back to the start of the current
         sub-path. It tries to add a straight line (but does not actually draw
         it) from the current point to the start. If the shape has already been
         closed or has only one point, this function does nothing.

        """
        return self._impl.close_path()

    def move_to(self, x, y):
        """Moves the starting point of a new sub-path to the (x, y) coordinates.

        Args:
            x (int): The x axis of the point
            y (int): The y axis of the point

        """
        return self._impl.move_to(x, y)

    def line_to(self, x, y):
        """Connects the last point with a line.

        Connects the last point in the sub-path to the (x, y) coordinates
        with a straight line (but does not actually draw it).

        Args:
            x (int): The x axis of the coordinate for the end of the line
            y (int): The y axis of the coordinate for the end of the line

        """
        self._impl.line_to(x, y)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        """Adds a cubic Bézier curve to the path.

        It requires three points. The first two points are control points
        and the third one is the end point. The starting point is the last
        point in the current path, which can be changed using moveTo() before
        creating the Bézier curve.

        Args:
            cp1x (int): x coordinate for the first control point
            cp1y (int): y coordinate for first control point
            cp2x (int): x coordinate for the second control point
            cp2y (int): y coordinate for the second control point
            x (int): x coordinate for the end point
            y (int): y coordinate for the end point

        """
        self._impl.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        """Adds a quadratic Bézier curve to the path.

        It requires two points. The first point is a control point and the
        second one is the end point. The starting point is the last point in the
        current path, which can be changed using moveTo() before creating the
        quadratic Bézier curve.

        Args:
            cpx (int): The x axis of the coordinate for the control point
            cpy (int): The y axis of the coordinate for the control point
            x (int): The x axis of the coordinate for the end point
            y (int): he y axis of the coordinate for the end point

        """
        self._impl.quadratic_curve_to(cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        """Adds an arc to the path.

        The arc is centered at (x, y) position with radius r starting at
        startAngle and ending at endAngle going in the given direction by
        anticlockwise (defaulting to clockwise).

        Args:
            x (int): The x coordinate of the arc's center
            y (int): The y coordinate of the arc's center
            radius (int): The arc's radius
            startangle (int): The angle (in radians) at which the arc starts,
                measured clockwise from the positive x axis
            endangle (int): The angle (in radians) at which the arc ends,
                measured clockwise from the positive x axis
            anticlockwise (bool): Optional, if true, causes the arc to be drawn
                counter-clockwise between the two angles instead of clockwise

        """
        self._impl.arc(x, y, radius, startangle, endangle, anticlockwise)

    def arc_to(self, x1, y1, x2, y2, radius):
        """ Adds an arc to the path connected by a line.

        Adds an arc to the path with the given control points and radius,
        connected to the previous point by a straight line.

        Args:
            x1 (int): The x axis of the coordinate for the first control point
            y1 (int): The y axis of the coordinate for the first control point
            x2 (int): The x axis of the coordinate for the second control point
            y2 (int): The y axis of the coordinate for the second control point
            radius (int): The arc's radius

        """
        self._impl.arc_to(x1, y1, x2, y2, radius)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        """Adds an ellipse to the path.

        The ellipse is centered at (x, y) position with the radii radiusx and radiusy
        starting at startAngle and ending at endAngle going in the given
        direction by anticlockwise (defaulting to clockwise).

        Args:
            x (int): The x axis of the coordinate for the ellipse's center
            y (int): The y axis of the coordinate for the ellipse's center
            radiusx (int): The ellipse's major-axis radius
            radiusy (int): The ellipse's minor-axis radius
            rotation (int): The rotation for this ellipse, expressed in radians
            startangle (int): The starting point in radians, measured from the x
                axis, from which it will be drawn
            endangle (int): The end ellipse's angle in radians to which it will
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
            x (int): x coordinate for the rectangle starting point
            y (int): y coordinate for the rectangle starting point
            width (int): The rectangle's width
            height (int): The rectangle's width

        Returns:

        """
        self._impl.rect(x, y, width, height)
