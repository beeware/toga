from colosseum import CSSNode


class Widget:
    '''This is the base widget implementation that all widgets in Toga
    derive from.

    It defines the interface for core functionality for children, styling,
    layout and ownership by specific App and Window.

    Apart from the above, this is an abstract implementation which must
    be made concrete by some platform-specific code for the _apply_layout
    method.

    :param id: An identifier for this widget.
    :param style: an optional style object. If no style is provided then a
                  new one will be created for the widget.
    '''
    def __init__(self, id=None, style=None, **config):
        self._id = id
        self._parent = None
        self._children = None
        self._window = None
        self._app = None
        self._impl = None
        self.__container = None
        self.dirty = True
        self._layout_in_progress = False
        self._config = config

        if style:
            self._style = style.apply(self)
        else:
            self._style = CSSNode(self)

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, id(self))

    @property
    def id(self):
        '''The node identifier.

        This id can be used to target CSS directives
        '''
        return self._id

    @property
    def style(self):
        '''The style object for this widget.
        '''
        return self._style

    @property
    def parent(self):
        '''The parent of this node.
        '''
        return self._parent

    @property
    def children(self):
        '''The children of this node.

        This *always* returns a list, even if the node is a leaf
        and cannot have children.
        '''
        if self._children is None:
            return []
        else:
            return self._children

    def add(self, child):
        '''Add a widget as a child of this one.

        Raises an error if this widget is a leaf, and cannot
        have children.
        '''
        if self._children is None:
            raise ValueError('Widget cannot have children')

        self._children.append(child)

        child.app = self.app
        child._parent = self

        if self._parent:
            self._parent.dirty = True

        self._add_child(child)

    @property
    def app(self):
        '''The App to which this widget belongs.
        '''
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Widget %r is already associated with an App" % self)
        self._app = app
        self._set_app(app)
        if self._children is not None:
            for child in self._children:
                child.app = app

    @property
    def window(self):
        '''The Window to which this widget belongs.
        '''
        return self._window

    @window.setter
    def window(self, window):
        self._window = window
        self._set_window(window)
        if self._children is not None:
            for child in self._children:
                child.window = window

    @property
    def _container(self):
        '''The display container to which this widget belongs.
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
        # print("UPDATE LAYOUT OF ", self, style)
        if self._layout_in_progress:
            return
        self._layout_in_progress = True

        self.style.set(**style)

        # Recompute layout for this widget
        self.style.recompute()

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

        See toga.Font.
        """
        self._set_font(font)
