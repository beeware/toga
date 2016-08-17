from colosseum import CSSNode


class Widget(object):
    '''This is the base widget implementation that all widgets in Toga
    derive from.

    It defines the interface for core functionality for children, styling,
    layout and ownership by specific App and Window.

    Apart from the above, this is an abstract implementation which must
    be made concrete by some platform-specific code for the _apply_layout
    method.

    :param style: an optional CSSNode object; if none is provided then a
                  new one will be created for the widget.
    '''
    def __init__(self, style=None):
        self._parent = None
        self._children = None
        self._window = None
        self._app = None
        self.dirty = True
        self._layout_in_progress = False

        if style:
            self._style = style.apply(self)
        else:
            self._style = CSSNode(self)

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, id(self))

    @property
    def style(self):
        '''The CSSNode style for this widget.
        '''
        return self._style

    @property
    def parent(self):
        '''The parent of this widget.
        '''
        return self._parent

    @property
    def children(self):
        '''The list of child Widgets for this widget.
        '''
        if self._children is None:
            return []
        else:
            return self._children

    def add(self, child):
        '''Add a new child Widget to this one.
        '''
        if self._children is None:
            raise ValueError('Widget cannot have children')
        self._children.append(child)
        child._parent = self._parent
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

    def _set_app(self, app):
        pass

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

    def _set_window(self, window):
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

        self.style.set(**style)

        # Recompute layout
        layout = self.style.layout

        self._update_child_layout(**style)

        # Set the frame for the widget to adhere to the new style.
        self._apply_layout(layout)

        self._layout_in_progress = False

    def _update_child_layout(self, **style):
        if self._children is not None:
            for child in self.children:
                # if child.is_container:
                child._update_layout()

    def _apply_layout(self):
        raise NotImplementedError('Implementation must define _apply_layout()')
