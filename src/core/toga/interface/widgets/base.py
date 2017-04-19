from builtins import id as identifier
from colosseum import CSS


class Point:
    def __init__(self, top, left):
        self.top = top
        self.left = left

    def __repr__(self):
        return '<Point (%s,%s)>' % (self.left, self.top)


class Layout:
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
    '''
    This is the base widget implementation that all widgets in Toga
    derive from.

    It defines the interface for core functionality for children, styling,
    layout and ownership by specific App and Window.

    Apart from the above, this is an abstract implementation which must
    be made concrete by some platform-specific code for the _apply_layout
    method.

    :param id:      An identifier for this widget.
    :type  id:      ``str``

    :param style:   An optional style object. If no style is provided then a
                    new one will be created for the widget.
    :type style:    :class:`colosseum.CSSNode`
    '''
    def __init__(self, id=None, style=None, **config):
        self._id = id if id else identifier(self)
        self._parent = None
        self._children = None
        self._window = None
        self._app = None
        self._impl = None
        self.__container = None
        self._layout_in_progress = False

        self._config = config

        self.layout = Layout(self)
        if style:
            self.style = style.copy()
        else:
            self.style = CSS()

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, id(self))

    @property
    def id(self):
        '''
        The node identifier. This id can be used to target CSS directives

        :rtype: ``str``
        '''
        return self._id

    @property
    def style(self):
        '''
        The style object for this widget.

        :return: The style for this widget
        :rtype: :class:`colosseum.CSSNode`
        '''
        return self._style

    @style.setter
    def style(self, value):
        self._style = value.bind(self)

    @property
    def parent(self):
        '''
        The parent of this node.

        :rtype: :class:`toga.Widget`
        '''
        return self._parent

    @property
    def children(self):
        '''
        The children of this node.

        This *always* returns a list, even if the node is a leaf
        and cannot have children.

        :rtype: ``list``
        :return: A list of the children for this widget
        '''
        if self._children is None:
            return []
        else:
            return self._children

    def add(self, child):
        '''
        Add a widget as a child of this one.

        Raises an :class:`ValueError` if this widget is a leaf, and cannot
        have children.

        :param child: The child to add to the widget
        :type  child: :class:`toga.Widget`
        '''
        if self._children is None:
            raise ValueError('Widget cannot have children')

        self._children.append(child)

        child.app = self.app
        child._parent = self

        if self.parent:
            self.parent.layout.dirty = True

        self._add_child(child)

    @property
    def app(self):
        '''
        The App to which this widget belongs.

        :rtype: :class:`toga.App`
        '''
        return self._app

    @app.setter
    def app(self, app):
        '''
        Set the app to which this widget belongs

        :param app: The Application host
        :type  app: :class:`toga.App`
        '''
        if self._app:
            raise Exception("Widget %r is already associated with an App" % self)
        if app:
            self._app = app
            self._set_app(app)
            if self._children is not None:
                for child in self._children:
                    child.app = app

    @property
    def window(self):
        '''
        The Window to which this widget belongs.

        :rtype: :class:`toga.Window`
        '''
        return self._window

    @window.setter
    def window(self, window):
        '''
        Set the Window to which this widget belongs.

        :param window: The new window
        :type  window: :class:`toga.Window`
        '''
        self._window = window
        self._set_window(window)
        if self._children is not None:
            for child in self._children:
                child.window = window

    @property
    def _container(self):
        '''
        The display container to which this widget belongs.
        '''
        return self.__container

    @_container.setter
    def _container(self, container):
        self.__container = container
        self._set_container(container)
        if self._children is not None:
            for child in self._children:
                child._container = container

    def _create(self):
        self.create()
        self._configure(**self._config)

    def _initialize(self, **initial):
        pass

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
        self._apply_layout()
        self._layout_in_progress = False

    def _update_child_layout(self):
        # print("UPDATE CHILD LAYOUT - widget")
        if self._children is not None:
            for child in self.children:
                # if child.is_container:
                child._update_layout()

    def set_font(self, font):
        """
        Set a font on this widget.

        :param font: The new font
        :type  font: :class:`toga.Font`
        """
        self._set_font(font)
