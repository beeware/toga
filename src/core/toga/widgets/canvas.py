from contextlib import contextmanager
from math import pi

from .base import Widget
from ..color import color as parse_color


class InterfaceMixin:
    def __init__(self, **kwargs):  # kwargs used to support multiple inheritance
        super().__init__(**kwargs)

        self.drawing_objects = []
        self._parent_context = None
        self._child_context = None
        self._canvas = None
        self._children_contexts = None

    ###########################################################################
    # Private methods to keep track of the canvas, automatically redraw it
    ###########################################################################

    @staticmethod
    def __set_canvas(node, canvas):
        """Propagate a canvas node change through a tree of contexts.

        Args:
            node: The context node to add.
            canvas: :class:`ResetTransform <ResetTransform>` object.

        """
        node._canvas = canvas
        for child in node.__children_contexts:
            node.__set_canvas(child, canvas)

    @property
    def __canvas(self):
        """The canvas of the tree containing this context.

        Returns:
            The canvas node. Returns self if this node *is* the canvas node.

        """
        return self._canvas if self._canvas else self

    @property
    def __parent_context(self):
        """ The parent of this node.

        Returns:
            The parent of this node. Returns None if this node is the canvas node.

        """
        return self._parent_context

    @property
    def __children_contexts(self):
        """The children of this node.

        This *always* returns a list, even if the node is a non-context drawing
        object and cannot have children.

        Returns:
            A list of the children contexts for this widget.

        """
        if self._children_contexts is None:
            return []
        else:
            return self._children_contexts

    def __add_child(self, child):
        """Add a context as a child of this one.

        Args:
            child: A context to add as a child to this context.

        Raises:
            ValueError: If this node is not a context, and cannot have children.

        """
        if self._children_contexts is None:
            raise ValueError('Cannot add children')

        self._children_contexts.append(child)
        child._parent_context = self
        self.__set_canvas(child, self.__canvas)

    def __add_drawing_object(self, drawing_object):
        """A drawing object to add to the drawing object stack on a context

        Args:
            drawing_object: (:obj:`Drawing Object`): The drawing object to add

        """
        self.drawing_objects.append(drawing_object)
        self.__redraw()

    def __redraw(self):
        """Force a redraw of the Canvas

        The Canvas will be automatically redrawn after adding or remove a
        drawing object. If you modify a drawing object, this method is used to
        force a redraw.

        """
        self._canvas._impl.redraw()

    ###########################################################################
    # Operations on drawing objects
    ###########################################################################

    def remove(self, drawing_object):
        """Remove a drawing object

        Args:
            drawing_object (:obj:'Drawing Object'): The drawing object to remove

        """
        self.drawing_objects.remove(drawing_object)
        self.__redraw()

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
        self.__add_drawing_object(context.drawing_objects)
        self.__add_child(context)
        yield context

    @contextmanager
    def fill(self, color=None, fill_rule='nonzero', preserve=False):
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
        if fill_rule is 'evenodd':
            fill = Fill(color, fill_rule, preserve)
        else:
            fill = Fill(color, 'nonzero', preserve)
        self.__add_drawing_object(fill.drawing_objects)
        self.__add_child(fill)
        new_path = NewPath()
        fill.__add_drawing_object(new_path)
        yield fill
        self.__add_drawing_object(fill)

    @contextmanager
    def stroke(self, color=None, line_width=2.0):
        """Constructs and yields a :class:`Stroke <Stroke>`.

        Args:
            color (str, optional): color value in any valid color format,
                default to black.
            line_width (float, optional): stroke line width, default is 2.0.

        Yields:
            :class:`Stroke <Stroke>` object.

        """
        stroke = Stroke(color, line_width)
        self.__add_drawing_object(stroke.drawing_objects)
        self.__add_child(stroke)
        yield stroke
        self.__add_drawing_object(stroke)

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
        self.__add_drawing_object(closed_path.drawing_objects)
        self.__add_child(closed_path)
        closed_path.move_to(x, y)
        yield closed_path
        self.__add_drawing_object(closed_path)

    ###########################################################################
    # Paths to draw with
    ###########################################################################

    def move_to(self, x, y):
        """Constructs and returns a :class:`MoveTo <MoveTo>`.

        Args:
            x (float): The x axis of the point.
            y (float): The y axis of the point.

        Returns:
            :class:`MoveTo <MoveTo>` object.

        """
        move_to = MoveTo(x, y)
        self.__add_drawing_object(move_to)
        return move_to

    def line_to(self, x, y):
        """Constructs and returns a :class:`LineTo <LineTo>`.

        Args:
            x (float): The x axis of the coordinate for the end of the line.
            y (float): The y axis of the coordinate for the end of the line.

        Returns:
            :class:`LineTo <LineTo>` object.

        """
        line_to = LineTo(x, y)
        self.__add_drawing_object(line_to)
        return line_to

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
        self.__add_drawing_object(bezier_curve_to)
        return bezier_curve_to

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
        self.__add_drawing_object(quadratic_curve_to)
        return quadratic_curve_to

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
        self.__add_drawing_object(arc)
        return arc

    def ellipse(self, x, y, radiusx, radiusy, rotation=0.0, startangle=0.0, endangle=2 * pi, anticlockwise=False):
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
        ellipse = Ellipse(x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise)
        self.__add_drawing_object(ellipse)
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
        self.__add_drawing_object(rect)
        return rect

    ###########################################################################
    # Transformations of a context
    ###########################################################################

    def rotate(self, radians):
        """Constructs and returns a :class:`Rotate <Rotate>`.

        Args:
            radians (float): The angle to rotate clockwise in radians.

        Returns:
            :class:`Rotate <Rotate>` object.

        """
        rotate = Rotate(radians)
        self.__add_drawing_object(rotate)
        return rotate

    def scale(self, sx, sy):
        """Constructs and returns a :class:`Scale <Scale>`.

        Args:
            sx (float): scale factor for the X dimension.
            sy (float): scale factor for the Y dimension.

        Returns:
            :class:`Scale <Scale>` object.

        """
        scale = Scale(sx, sy)
        self.__add_drawing_object(scale)
        return scale

    def translate(self, tx, ty):
        """Constructs and returns a :class:`Translate <Translate>`.

        Args:
            tx (float): X value of coordinate.
            ty (float): Y value of coordinate.

        Returns:
            :class:`Translate <Translate>` object.

        """
        translate = Translate(tx, ty)
        self.__add_drawing_object(translate)
        return translate

    def reset_transform(self):
        """Constructs and returns a :class:`ResetTransform <ResetTransform>`.

        Returns:
            :class:`ResetTransform <ResetTransform>` object.

        """
        reset_transform = ResetTransform()
        self.__add_drawing_object(reset_transform)
        return reset_transform

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
        write_text = WriteText(text, x, y, font)
        self.__add_drawing_object(write_text)
        return write_text


class Canvas(InterfaceMixin, Widget):
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

        self._canvas = self

        # Create a platform specific implementation of Canvas
        self._impl = self.factory.Canvas(interface=self)
        self._impl.set_context_root(self.drawing_objects)

        # Canvas can have children contexts
        self._children_contexts = []


class Context(InterfaceMixin, object):
    """The user-created :class:`Context <Context>` drawing object to populate a
    drawing with visual context.

    The top left corner of the canvas must be painted at the origin of the
    context and is sized using the rehint() method.

    """
    def __init__(self):
        super().__init__()

        # Context can have children contexts
        self._children_contexts = []

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.context()


class Fill(InterfaceMixin, object):
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
    def __init__(self, color=None, fill_rule='nonzero', preserve=False):
        super().__init__()
        if color:
            self.color = parse_color(color)
        else:
            self.color = None
        self.fill_rule = fill_rule
        self.preserve = preserve

        # Fill context can have children contexts
        self._children_contexts = []

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.fill(self.color, self.fill_rule, self.preserve)

    def modify(self, color=None, fill_rule='nonzero', preserve=False):
        """Modify the fill properties after it has been drawn with.

        Args:
            color (str, optional): Color value in any valid color format,
                default to black.
            fill_rule (str, optional): 'nonzero' is the non-zero winding rule and
                                       'evenodd' is the even-odd winding rule.
            preserve (bool, optional): Preserves the path within the Context.

        """
        if color:
            self.color = parse_color(color)
        else:
            self.color = None
        self.fill_rule = fill_rule
        self.preserve = preserve


class Stroke(InterfaceMixin, object):
    """A user-created :class:`Stroke <Stroke>` drawing object for a stroke context.

    A drawing operator that strokes the current path according to the
    current line style settings.

    Args:
        color (str, optional): Color value in any valid color format,
            default to black.
        width (float, optional): Stroke line width, default is 2.0.

    """
    def __init__(self, color=None, width=2.0):
        super().__init__()
        if color:
            self.color = parse_color(color)
        else:
            self.color = None
        self.width = width

        # Stroke context can have children contexts
        self._children_contexts = []

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.stroke(self.color, self.width)

    def modify(self, color=None, width=2.0):
        """Modify the stroke properties after it has been drawn with.

        Args:
            color (str, optional): Color value in any valid color format,
                default to black.
            width (float, optional): Stroke line width, default is 2.0.

        """
        if color:
            self.color = parse_color(color)
        else:
            self.color = None
        self.width = width


class ClosedPath(InterfaceMixin, object):
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

        # ClosedPath context can have children contexts
        self._children_contexts = []

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.closed_path(self.x, self.y)


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

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.move_to(self.x, self.y)

    def modify(self, x, y):
        """Modify the move to operation after it has been drawn.

        Args:
            x (float): The x axis of the point.
            y (float): The y axis of the point.

        """
        self.x = x
        self.y = y


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

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.line_to(self.x, self.y)

    def modify(self, x, y):
        """Modify the line to operation after it has been drawn.

        Args:
            x (float): The x axis of the coordinate for the end of the line.
            y (float): The y axis of the coordinate for the end of the line.

        """
        self.x = x
        self.y = y


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

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.bezier_curve_to(self.cp1x, self.cp1y, self.cp2x, self.cp2y, self.x, self.y)

    def modify(self, cp1x, cp1y, cp2x, cp2y, x, y):
        """Modify the rectangle after it has been drawn.

        Args:
            cp1x (float): x coordinate for the first control point.
            cp1y (float): y coordinate for first control point.
            cp2x (float): x coordinate for the second control point.
            cp2y (float): y coordinate for the second control point.
            x (float): x coordinate for the end point.
            y (float): y coordinate for the end point.

        """
        self.cp1x = cp1x
        self.cp1y = cp1y
        self.cp2x = cp2x
        self.cp2y = cp2y
        self.x = x
        self.y = y


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

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.quadratic_curve_to(self.cpx, self.cpy, self.x, self.y)

    def modify(self, cpx, cpy, x, y):
        """Modify the rectangle after it has been drawn.

        Args:
            cpx (float): The x axis of the coordinate for the control point.
            cpy (float): The y axis of the coordinate for the control point.
            x (float): The x axis of the coordinate for the end point.
            y (float): he y axis of the coordinate for the end point.

        """
        self.cpx = cpx
        self.cpy = cpy
        self.x = x
        self.y = y


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
        """Allow the implementation to callback the Class instance.

        """
        impl.ellipse(
            self.x, self.y, self.radiusx, self.radiusy, self.rotation, self.startangle,
            self.endangle, self.anticlockwise
        )

    def modify(self, x, y, radiusx, radiusy, rotation=0.0, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        """Modify the ellipse after it has been drawn.

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
        """
        self.x = x
        self.y = y
        self.radiusx = radiusx
        self.radiusy = radiusy
        self.rotation = rotation
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise


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
    def __init__(self, x, y, radius, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.arc(self.x, self.y, self.radius, self.startangle, self.endangle, self.anticlockwise)

    def modify(self, x, y, radius, startangle=0.0, endangle=2 * pi, anticlockwise=False):
        """Modify the arc after it has been drawn.

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
        self.x = x
        self.y = y
        self.radius = radius
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise


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

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.rect(self.x, self.y, self.width, self.height)

    def modify(self, x, y, width, height):
        """Modify the rectangle after it has been drawn.

        Args:
            x (float): x coordinate for the rectangle starting point.
            y (float): y coordinate for the rectangle starting point.
            width (float): The rectangle's width.
            height (float): The rectangle's width.

        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Rotate:
    """A user-created :class:`Rotate <Rotate>` to add context rotation.

    Modifies the current transformation matrix (CTM) by rotating the
    user-space axes by angle radians. The rotation of the axes takes places
    after any existing transformation of user space. The rotation center
    point is always the canvas origin. To change the center point, move the
    canvas by using the translate() method.

    Args:
        radians (float): The angle to rotate clockwise in radians.

    """
    def __init__(self, radians):
        self.radians = radians

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.rotate(self.radians)

    def modify(self, radians):
        """Modify the rotation after it has been drawn.

        Args:
            radians (float): The angle to rotate clockwise in radians.

        """
        self.radians = radians


class Scale:
    """A user-created :class:`Scale <Scale>` to add context scaling.

    Modifies the current transformation matrix (CTM) by scaling the X and Y
    user-space axes by sx and sy respectively. The scaling of the axes takes
    place after any existing transformation of user space.

    Args:
        sx (float): scale factor for the X dimension.
        sy (float): scale factor for the Y dimension.

    """
    def __init__(self, sx, sy):
        self.sx = sx
        self.sy = sy

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.scale(self.sx, self.sy)

    def modify(self, sx, sy):
        """Modify the scale after it has been drawn.

        Args:
            sx (float): scale factor for the X dimension.
            sy (float): scale factor for the Y dimension.

        """
        self.sx = sx
        self.sy = sy


class Translate:
    """A user-created :class:`Translate <Translate>` to translate the context.

    Modifies the current transformation matrix (CTM) by translating the
    user-space origin by (tx, ty). This offset is interpreted as a
    user-space coordinate according to the CTM in place before the new call
    to translate(). In other words, the translation of the user-space origin
    takes place after any existing transformation.

    Args:
        tx (float): X value of coordinate.
        ty (float): Y value of coordinate.

    """
    def __init__(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.translate(self.tx, self.ty)

    def modify(self, tx, ty):
        """Modify the translation after it has been drawn.

        Args:
            tx (float): X value of coordinate.
            ty (float): Y value of coordinate.

        """
        self.tx = tx
        self.ty = ty


class ResetTransform:
    """A user-created :class:`ResetTransform <ResetTransform>` to reset the
    context.

    Resets the current transformation Matrix (CTM) by setting it equal to
    the identity matrix. That is, the user-space and device-space axes will
    be aligned and one user-space unit will transform to one device-space
    unit.

    """
    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.reset_transform()


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

    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.write_text(self.text, self.x, self.y, self.font)

    def modify(self, text, x, y, font):
        """Modify the text after it has been drawn.

        Args:
            text (string): The text to fill.
            x (float, optional): The x coordinate of the text. Default to 0.
            y (float, optional): The y coordinate of the text. Default to 0.
            font (:class:`toga.Font`, optional): The font to write with.

        """
        self.text = text
        self.x = x
        self.y = y
        self.font = font


class NewPath:
    """A user-created :class:`NewPath <NewPath>` to add a new path.

    """
    def __call__(self, impl):
        """Allow the implementation to callback the Class instance.

        """
        impl.new_path()
