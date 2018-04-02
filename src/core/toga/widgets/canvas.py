from contextlib import contextmanager
from math import pi

from .base import Widget


class Canvas(Widget):
    """Create new canvas

    Args:
        id (str):  An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no
            style is provided then a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional &
            normally not needed)
    """

    def __init__(self, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of Canvas
        self._impl = self.factory.Canvas(interface=self)

        self.context_root = []
        self._impl.set_context_root(self.context_root)
        self.drawing_objects = self.context_root
    
    def _add(self, drawing_object):
        self.drawing_objects.append(drawing_object)
        self._impl.redraw()

    def remove(self, drawing_object):
        """Remove a drawing object
        
        Args:
            drawing_object (:obj:'Drawing Object'): The drawing object to remove 

        """
        self.drawing_objects.remove(drawing_object)
        self._impl.redraw()

    def create_context(self):
        """Create a new context to draw to

        """
        context = Context()
        self._add(context.drawing_objects)
        return context

    @contextmanager
    def context(self, context):
        """The context of the Canvas to draw to

        Makes use of an existing context. The top left corner of the canvas must
        be painted at the origin of the context and is sized using the rehint()
        method.

        Args:
            context (:obj:`Context`): The context object to use

        """
        self.drawing_objects = context.drawing_objects
        yield
        self.drawing_objects = self.context_root

    # Paths

    @contextmanager
    def closed_path(self, x, y):
        """Creates a new path and then closes it

        Args:
            x (float): The x axis of the beginning point
            y (float): The y axis of the beginning point

        Yields: None

        """
        self.move_to(x, y)
        yield
        closed_path = ClosedPath(x, y)
        self._add(closed_path)
        return closed_path

    def move_to(self, x, y):
        """Moves the starting point of a new sub-path to the (x, y) coordinates.

        Args:
            x (float): The x axis of the point
            y (float): The y axis of the point

        """
        move_to = MoveTo(x, y)
        self._add(move_to)
        return move_to

    def line_to(self, x, y):
        """Connects the last point with a line.

        Connects the last point in the sub-path to the (x, y) coordinates
        with a straight line (but does not actually draw it).

        Args:
            x (float): The x axis of the coordinate for the end of the line
            y (float): The y axis of the coordinate for the end of the line

        """
        line_to = LineTo(x, y)
        self._add(line_to)
        return line_to

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
        bezier_curve_to = BezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)
        self._add(bezier_curve_to)
        return bezier_curve_to

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
        quadratic_curve_to = QuadraticCurveTo(cpx, cpy, x, y)
        self._add(quadratic_curve_to)
        return quadratic_curve_to

    def arc(self, x, y, radius, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        """Adds an arc to the path.

        The arc is centered at (x, y) position with radius r starting at
        startAngle and ending at endAngle going in the given direction by
        anticlockwise (defaulting to clockwise).

        Args:
            x (float): The x coordinate of the arc's center
            y (float): The y coordinate of the arc's center
            radius (float): The arc's radius
            startangle (float, optional): The angle (in radians) at which the
                arc starts, measured clockwise from the positive x axis,
                default 0.0
            endangle (float, optional): The angle (in radians) at which the arc ends,
                measured clockwise from the positive x axis, default 2*pi
            anticlockwise (bool, optional): If true, causes the arc to be drawn
                counter-clockwise between the two angles instead of clockwise,
                default false

        """
        arc = Arc(x, y, radius, startangle, endangle, anticlockwise)
        self._add(arc)
        return arc

    def ellipse(self, x, y, radiusx, radiusy, rotation=0.0, startangle=0.0, endangle=2 * pi,
                anticlockwise=False):
        """Adds an ellipse to the path.

        The ellipse is centered at (x, y) position with the radii radiusx and radiusy
        starting at startAngle and ending at endAngle going in the given
        direction by anticlockwise (defaulting to clockwise).

        Args:
            x (float): The x axis of the coordinate for the ellipse's center
            y (float): The y axis of the coordinate for the ellipse's center
            radiusx (float): The ellipse's major-axis radius
            radiusy (float): The ellipse's minor-axis radius
            rotation (float, optional): The rotation for this ellipse, expressed in radians, default 0.0
            startangle (float, optional): The starting point in radians, measured from the x
                axis, from which it will be drawn, default 0.0
            endangle (float, optional): The end ellipse's angle in radians to which it will
                be drawn, default 2*pi
            anticlockwise (bool, optional): If true, draws the ellipse
                anticlockwise (counter-clockwise) instead of clockwise, default false

        """
        ellipse = Ellipse(x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise)
        self._add(ellipse)
        return ellipse

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
        rect = Rect(x, y, width, height)
        self._add(rect)
        return rect

    # Drawing Paths

    @contextmanager
    def fill(self, color=None, fill_rule='nonzero', preserve=False):
        """Fills the subpaths with the current fill style

        A drawing operator that fills the current path according to the current
        fill rule, (each sub-path is implicitly closed before being filled).

        Args:
            fill_rule (str, optional): 'nonzero' is the non-zero winding rule and
                                       'evenodd' is the even-odd winding rule
            preserve (bool, optional): Preserves the path within the Context
            color (str, optional): CSS color value or in rgba(0, 0, 0, 1)
                format, default to black

        Yields: None

        """
        new_path = NewPath()
        self._add(new_path)
        yield
        if fill_rule is 'evenodd':
            fill = Fill(color, fill_rule, preserve)
            self._add(fill)
            return fill
        else:
            fill = Fill(color, 'nonzero', preserve)
            self._add(fill)
            return fill

    @contextmanager
    def stroke(self, color=None, line_width=2.0):
        """Strokes the subpaths with the current stroke style

        A drawing operator that strokes the current path according to the
        current line style settings.

        Args:
            color (str): CSS color value or in rgba(0, 0, 0, 1) format, default
                to black
            line_width (float, optional): stroke line width, default is 2.0

        Yields: None

        """
        yield
        stroke = Stroke(color, line_width)
        self._add(stroke)
        return stroke

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
        rotate = Rotate(radians)
        self._add(rotate)
        return rotate

    def scale(self, sx, sy):
        """Adds a scaling transformation to the canvas

        Modifies the current transformation matrix (CTM) by scaling the X and Y
        user-space axes by sx and sy respectively. The scaling of the axes takes
        place after any existing transformation of user space.

        Args:
            sx (float): scale factor for the X dimension
            sy (float): scale factor for the Y dimension

        """
        scale = Scale(sx, sy)
        self._add(scale)
        return scale

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
        translate = Translate(tx, ty)
        self._add(translate)
        return translate

    def reset_transform(self):
        """Reset the current transform by the identity matrix

        Resets the current transformation Matrix (CTM) by setting it equal to
        the identity matrix. That is, the user-space and device-space axes will
        be aligned and one user-space unit will transform to one device-space
        unit.

        """
        reset_transform = ResetTransform()
        self._add(reset_transform)
        return reset_transform

    # Text

    def write_text(self, text, x=0, y=0, font=None):
        """Writes a given text

        Writes a given text at the given (x,y) position. If no font is provided,
        then it will use the font assigned to the Canvas Widget, if it exists,
        or use the default font if there is no font assigned.

        Args:
            text (string): The text to fill.
            x (float, optional): The x coordinate of the text. Default to 0.
            y (float, optional): The y coordinate of the text. Default to 0.
            font (:class:`toga.Font`, optional): The font to write with.

        """
        write_text = WriteText(text, x, y, font)
        self._add(write_text)
        return write_text


class Context:
    def __init__(self):
        self.drawing_objects = []

    def __call__(self, impl):
        impl.context()


class ClosedPath:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self, impl):
        impl.closed_path(self.x, self.y)


class MoveTo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self, impl):
        impl.move_to(self.x, self.y)


class LineTo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self, impl):
        impl.line_to(self.x, self.y)


class BezierCurveTo:
    def __init__(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.cp1x = cp1x
        self.cp1y = cp1y
        self.cp2x = cp2x
        self.cp2y = cp2y
        self.x = x
        self.y = y

    def __call__(self, impl):
        impl.bezier_curve_to(self.cp1x, self.cp1y, self.cp2x, self.cp2y, self.x, self.y)


class QuadraticCurveTo:
    def __init__(self, cpx, cpy, x, y):
        self.cpx = cpx
        self.cpy = cpy
        self.x = x
        self.y = y

    def __call__(self, impl):
        impl.quadratic_curve_to(self.cpx, self.cpy, self.x, self.y)


class Ellipse:
    def __init__(self, x, y, radiusx, radiusy, rotation=0.0, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        self.x = x
        self.y = y
        self.radiusx = radiusx
        self.radiusy = radiusy
        self.rotation = rotation
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __call__(self, impl):
        impl.ellipse(
            self.x, self.y, self.radiusx, self.radiusy, self.rotation, self.startangle,
            self.endangle, self.anticlockwise
        )


class Arc:
    def __init__(self, x, y, radius, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __call__(self, impl):
        impl.arc(self.x, self.y, self.radius, self.startangle, self.endangle, self.anticlockwise)


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __call__(self, impl):
        impl.rect(self.x, self.y, self.width, self.height)


class Fill:
    def __init__(self, color=None, fill_rule='nonzero', preserve=False):
        self.color = color
        self.fill_rule = fill_rule
        self.preserve = preserve

    def __call__(self, impl):
        impl.fill(self.color, self.fill_rule, self.preserve)


class Stroke:
    def __init__(self, color=None, width=2.0):
        self.color = color
        self.width = width

    def __call__(self, impl):
        impl.stroke(self.color, self.width)


class Rotate:
    def __init__(self, rotate):
        self.rotate = rotate

    def __call__(self, impl):
        impl.rotate(self.rotate)


class Scale:
    def __init__(self, sx, sy):
        self.sx = sx
        self.sy = sy

    def __call__(self, impl):
        impl.scale(self.sx, self.sy)


class Translate:
    def __init__(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def __call__(self, impl):
        impl.translate(self.tx, self.ty)


class ResetTransform:
    def __call__(self, impl):
        impl.reset_transform()


class WriteText:
    def __init__(self, text, x, y, font):
        self.text = text
        self.x = x
        self.y = y
        self.font = font

    def __call__(self, impl):
        impl.write_text(self.text, self.x, self.y, self.font)


class NewPath:
    def __call__(self, impl):
        impl.new_path()
