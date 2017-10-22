from .base import Widget


class Canvas(Widget):
    """Create new canvas

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


class Context2D(Widget):
    """Provide 2D rendering context for a canvas that you can draw on

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
        self._impl = self.factory.Context2D(interface=self)
        self.rehint()

    # Canvas State

    def save(self):
        """Push context to a stack

        Restores Context to the state saved by a preceding call to save() and
        removes that state from the stack of saved states.

        """
        self._impl.save()

    def restore(self):
        """Restore to the saved state

        Makes a copy of the current state of Context and saves it on an internal
        stack of saved states. When restore() is called, Context will be
        restored to the saved state. Multiple calls to save() and restore() can
        be nested; each call to restore() restores the state from the matching
        paired save().

        """
        self._impl.restore()

    def release(self):
        """Release the context when it no longer needed

        """
        self._impl.release()

    # Line Styles

    def line_width(self, width=2.0):
        """Set width of lines

        Args:
            width (float): line width

        """
        self._impl.line_width(width)

    # Fill and Stroke Styles

    def fill_style(self, color='None', r=0.0, g=0.0, b=0.0, a=0.0):
        """Color to use inside shapes

        Currently supports color, in the future could support gradient and
        pattern. A named color or RGBA value must be passed, or default
        to black.
        Args:
            color (str): CSS color value
            r (float): RGBA red value
            g (float): RGBA green value
            b (float): RGBA blue value
            a (float): RGBA alpha value

        """
        self._impl.fill_style(color)

    def stroke_style(self, color='None', r=0.0, g=0.0, b=0.0, a=1.0):
        """Color to use for lines around shapes

        Currently supports color, in the future could support gradient and
        pattern. A named color or RGBA value must be passed, or default to
        black.
        Args:
            color (str): CSS color value
            r (float): RGBA red value
            g (float): RGBA green value
            b (float): RGBA blue value
            a (float): RGBA alpha value

        """
        self._impl.stroke_style(color)

    # Paths

    def begin_path(self):
        """Create new path

        """
        self._impl.begin_path()

    def close_path(self):
        """Closes a path

         Causes the point of the pen to move back to the start of the current
         sub-path. It tries to add a straight line (but does not actually draw
         it) from the current point to the start. If the shape has already been
         closed or has only one point, this function does nothing.

        """
        self._impl.close_path()

    def move_to(self, x, y):
        """Moves the starting point of a new sub-path to the (x, y) coordinates.

        Args:
            x (int): The x axis of the point
            y (int): The y axis of the point

        """
        self._impl.move_to(x, y)

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

    def arc(self, x, y, radius, startangle, endangle, anticlockwise=False):
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

        """
        self._impl.rect(x, y, width, height)

    # Drawing Paths

    def fill(self, fill_rule='nonzero', preserve=False):
        """Fills the subpaths with the current fill style

        A drawing operator that fills the current path according to the current
        fill rule, (each sub-path is implicitly closed before being filled).

        Args:
            fill_rule (str): 'nonzero' is the non-zero winding rule and
                             'evenodd' is the even-odd winding rule
            preserve (bool): Preserves the path within the Context

        """
        if fill_rule is 'evenodd':
            self._impl.fill(fill_rule, preserve)
        else:
            self._impl.fill('nonzero', preserve)

    def stroke(self):
        """Strokes the subpaths with the current stroke style

        A drawing operator that strokes the current path according to the
        current line style settings.

        """
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

class Matrix(Widget):
    """Defines the transformation from user-space to device-space coordinates

    Args:

        xx (float): xx component of the affine transformation
        yx (float): yx component of the affine transformation
        xy (float): xy component of the affine transformation
        yy (float): yy component of the affine transformation
        x0 (float): X translation component of the affine transformation
        y0 (float): Y translation component of the affine transformation

    """

    def __init__(self, id=None, style=None, xx=1.0, yx=0.0, xy=0.0, yy=1.0, x0=0.0, y0=0.0, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.Matrix(interface=self)

    def transform_point(self, x, y):
        """Transforms the point (x, y) by Matrix

        Args:
            x (float): X position
            y (float): Y position

        Returns:
            tuple: the transformed point (x, y)

        """
        return self._impl.transform_point(x, y)

