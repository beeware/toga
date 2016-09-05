from colosseum import CSSNode


class Widget:
    def __init__(self, id=None, style=None):
        self._id = id
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
    def id(self):
        return self._id

    @property
    def style(self):
        return self._style

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        if self._children is None:
            return []
        else:
            return self._children

    def add(self, child):
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
        return self._window

    @window.setter
    def window(self, window):
        self._window = window
        self._set_window(window)
        if self._children is not None:
            for child in self._children:
                child.window = window

    def _update_layout(self, **style):
        """Force a layout update on the widget.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        # print("UPDATE LAYOUT OF ", self)
        if self._layout_in_progress:
            return
        self._layout_in_progress = True

        self.style.set(**style)

        # Recompute layout
        self.style.recompute()

        self._update_child_layout()

        # Set the frame for the widget to adhere to the new style.
        self._apply_layout()

        self._layout_in_progress = False

    def _update_child_layout(self):
        # print("UPDATE CHILD LAYOUT - widget")
        if self._children is not None:
            for child in self.children:
                # if child.is_container:
                child._update_layout()
