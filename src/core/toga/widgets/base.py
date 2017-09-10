from builtins import id as identifier
from colosseum import CSS
from ..platform import get_platform_factory

class Point:
    """ The :obj:`Point class hold the x and y coordinates of a point.

    Args:
        top (int or float): The y coordinate of the point.
        left (int or float): The x coordinate of the point.
    """

    def __init__(self, top, left):
        self.top = top
        self.left = left

    def __repr__(self):
        return '<Point (%s,%s)>' % (self.left, self.top)


class Layout:
    """ The :obj:`Layout` is the mathematical representation of a box.
    It has attributes like width, height, top, left to describe its bounding box.
    With the :obj:`dirty` flag it can track whether or not its as well as the
    layout of all children needs to be reevaluated.

    Args:
        node (:obj:`toga.Widget`): The widget that the layout should be attached to.
        width (int): The width of the box.
        height (int): The height of the box.
        top (int): The y coordinate of the top side of the box.
        left (int): The x coordinate of the left side of the box.
    """

    def __init__(self, node, width=None, height=None, top=0, left=0):
        self.node = node
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self._dirty = True

    def __repr__(self):
        if self.node:
            return '<Layout%s (%sx%s @ %s,%s)>' % (
                {
                    True: ' (dirty)',
                    False: '',
                    None: ' (evaluating)'
                }[self._dirty],
                self.width, self.height,
                self.absolute.left, self.absolute.top
            )
        else:
            return '<Layout%s (%sx%s @ %s,%s)>' % (
                {
                    True: ' (dirty)',
                    False: '',
                    None: ' (evaluating)'
                }[self._dirty],
                self.width, self.height,
                self.left, self.top
            )

    def __eq__(self, value):
        return all([
            self.width == value.width,
            self.height == value.height,
            self.top == value.top,
            self.left == value.left
        ])

    def reset(self):
        self.width = None
        self.height = None
        self.top = 0
        self.left = 0

    ######################################################################
    # Layout dirtiness tracking.
    #
    # If dirty == True, the layout is known to be invalid.
    # If dirty == False, the layout is known to be good.
    # If dirty is None, the layout is currently being re-evaluated.
    ######################################################################
    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        for child in self.node.children:
            child.layout.dirty = value

    ######################################################################
    # Implied geometry properties
    ######################################################################
    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def absolute(self):
        if self.node.parent:
            parent_layout = self.node.parent.layout
            return Point(
                top=parent_layout.origin.top + parent_layout.top + self.top,
                left=parent_layout.origin.left + parent_layout.left + self.left,
            )
        else:
            return Point(top=self.top, left=self.left)

    @property
    def origin(self):
        if self.node.parent:
            parent_layout = self.node.parent.layout
            return Point(
                top=parent_layout.origin.top + parent_layout.top,
                left=parent_layout.origin.left + parent_layout.left,
            )
        else:
            return Point(top=0, left=0)


class Widget:
    """ This is the base widget implementation that all widgets in Toga
    derive from.

    It defines the interface for core functionality for children, styling,
    layout and ownership by specific App and Window.

    Apart from the above, this is an abstract implementation which must
    be made concrete by some platform-specific code for the _apply_layout
    method.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`colosseum.CSSNode`): An optional style object.
            If no style is provided then a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name (optional & normally not needed).
    """

    def __init__(self, id=None, style=None, factory=None):
        self._id = id if id else identifier(self)
        self._parent = None
        self._children = None
        self._window = None
        self._app = None
        self._impl = None
        self._layout_in_progress = False

        self.layout = Layout(self)
        if style:
            self.style = style.copy()
        else:
            self.style = CSS()

        self._font = None

        self.factory = get_platform_factory(factory)

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, id(self))

    @property
    def id(self):
        """ The node identifier. This id can be used to target CSS directives

        Returns:
            The widgets identifier as a ``str``.
        """
        return self._id

    @property
    def parent(self):
        """ The parent of this node.

        Returns:
            The parent :class:`toga.Widget`.
        """
        return self._parent

    @property
    def children(self):
        """ The children of this node.
        This *always* returns a list, even if the node is a leaf
        and cannot have children.

        Returns:
            A list of the children for this widget.
        """
        if self._children is None:
            return []
        else:
            return self._children

    def add(self, child):
        """ Add a widget as a child of this one.
        Args:
            child (:class:`toga.Widget`): A widget to add as a child to this widget.

        Raises:
            ValueError: If this widget is a leaf, and cannot have children.
        """
        if self._children is None:
            raise ValueError('Widget cannot have children')

        self._children.append(child)

        child.app = self.app
        child._parent = self

        if self.parent:
            self.parent.layout.dirty = True
        if self._impl:
            self._impl.add_child(child._impl)

    @property
    def app(self):
        """ The App to which this widget belongs.
        On setting the app we also iterate over all children of this widget and set them to the same app.

        Returns:
            The :class:`toga.App` to which this widget belongs.

        Raises:
            ValueError: If the widget is already associated with another app.
        """
        return self._app

    @app.setter
    def app(self, app):
        if self._app is not None:
            if self._app != app:
                raise ValueError("Widget %s is already associated with an App" % self)
        elif app is not None:
            self._app = app
            self._impl.set_app(app)
            if self._children is not None:
                for child in self._children:
                    child.app = app

    @property
    def window(self):
        """ The Window to which this widget belongs.
        On setting the window, we automatically update all children of this widget to belong to the same window.

        Returns:
            The :class:`toga.Window` to which the widget belongs.
        """
        return self._window

    @window.setter
    def window(self, window):
        self._window = window
        if self._impl:
            self._impl.set_window(window)
        if self._children is not None:
            for child in self._children:
                child.window = window

    @property
    def style(self):
        """ The style object for this widget.

        Returns:
            The style object :class:`colosseum.CSSNode` of the widget.
        """
        return self._style

    @style.setter
    def style(self, value):
        self._style = value.bind(self)

    @property
    def font(self):
        """ Font the widget.

        Returns:
            The :class:`toga.Font` of the widget.
        """
        return self._font

    @font.setter
    def font(self, font):
        self._font = font
        self._impl.set_font(font)

    def rehint(self):
        self._impl.rehint()

    def _update_layout(self, **style):
        """Force a layout update on the widget.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        if self._layout_in_progress:
            return
        self._layout_in_progress = True

        if style:
            self.style.set(**style)

        # Recompute layout for this widget
        self.style.apply()

        # Update the layout parameters for all children.
        # This will also perform a leaf-first update of
        # the constraint on each widget.
        self._update_child_layout()

        # Set the constraints the widget to adhere to the new style.
        self._impl.apply_layout()
        self._impl.apply_sub_layout()

        self._layout_in_progress = False

    def _update_child_layout(self):
        if self._children is not None:
            for child in self.children:
                child._update_layout()
                # # FIXME some wigets need their _update_child_layout() function get called.
                # try:
                #     child._impl._update_child_layout()
                # except:
                #     pass
