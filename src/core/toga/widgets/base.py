from builtins import id as identifier

from travertino.node import Node

from toga.platform import get_platform_factory
from toga.style import Pack, TogaApplicator


class Widget(Node):
    """ This is the base widget implementation that all widgets in Toga
    derive from.

    It defines the interface for core functionality for children, styling,
    layout and ownership by specific App and Window.

    Apart from the above, this is an abstract implementation which must
    be made concrete by some platform-specific code for the _apply_layout
    method.

    Args:
        id (str): An identifier for this widget.
        enabled (bool): Whether or not interaction with the button is possible, defaults to `True`.
        style: An optional style object.
            If no style is provided then a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name (optional & normally not needed).
    """

    def __init__(self, id=None, enabled=True, style=None, factory=None):
        super().__init__(
            style=style if style else Pack(),
            applicator=TogaApplicator(self)
        )

        self._id = str(id) if id else str(identifier(self))
        self._window = None
        self._app = None
        self._impl = None

        self._enabled = enabled

        self.factory = get_platform_factory(factory)

    def __repr__(self):
        return "<%s:0x%x>" % (self.__class__.__name__, identifier(self))

    @property
    def id(self):
        """The node identifier. This id can be used to target styling directives

        Returns:
            The widgets identifier as a ``str``.
        """
        return self._id

    def add(self, *children):
        """Add nodes as children of this one. If a node already has a different parent,
        it will be moved over. This does nothing if a node already is a child of this node.

        Args:
            children: Nodes to add as children of this node.

        Raises:
            ValueError: If this node is a leaf, and cannot have children.
        """
        for child in children:
            if child.parent is not self:

                # remove from old parent
                if child.parent:
                    child.parent.remove(child)

                # add to new parent
                super().add(child)

                # set app and window
                child.app = self.app
                child.window = self.window

                if self._impl:
                    self._impl.add_child(child._impl)

        if self.window:
            self.window.content.refresh()

    def insert(self, index, child):
        """Insert a node as a child of this one. If the node already has a different
        parent, it will be moved over. This does nothing if the node already is a child of
        this node.

        Args:
            index: Position of child node.
            child: A node to insert as a child of this node.

        Raises:
            ValueError: If this node is a leaf, and cannot have children.
        """
        if child.parent is not self:

            # remove from old parent
            if child.parent:
                child.parent.remove(child)

            # add to new parent
            super().insert(index, child)

            # set app and window
            child.app = self.app
            child.window = self.window

            if self._impl:
                self._impl.insert_child(index, child._impl)

        if self.window:
            self.window.content.refresh()

    def remove(self, *children):
        """Remove child nodes of this node. This does nothing if a given node is not a
        child of this node.

        Args:
            children: Child nodes to remove.

        Raises:
            ValueError: If this node is a leaf, and cannot have children.
        """
        for child in children:
            if child.parent is self:
                super().remove(child)

                child.app = None
                child.window = None

                if self._impl:
                    self._impl.remove_child(child._impl)

        if self.window:
            self.window.content.refresh()

    @property
    def app(self):
        """The App to which this widget belongs.
        On setting the app we also iterate over all children of this widget and
        set them to the same app.

        Returns:
            The :class:`toga.App` to which this widget belongs.

        Raises:
            ValueError: If the widget is already associated with another app.
        """
        return self._app

    @app.setter
    def app(self, app):
        # raise an error when we already have an app and attempt to override it
        # with a different app
        if self._app and app and self._app != app:
            raise ValueError("Widget %s is already associated with an App" % self)
        elif self._impl:
            self._app = app
            self._impl.set_app(app)
            for child in self.children:
                child.app = app

        # Provide an extension point for widgets with
        # more complex widget heirarchies
        self._set_app(app)

    def _set_app(self, app):
        pass

    @property
    def window(self):
        """The Window to which this widget belongs.
        On setting the window, we automatically update all children of this
        widget to belong to the same window.

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

        # Provide an extension point for widgets with
        # more complex widget heirarchies
        self._set_window(window)

    def _set_window(self, window):
        pass

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = bool(value)
        self._impl.set_enabled(value)

    def refresh(self):
        """Refresh the layout and appearance of the tree this node is contained in."""
        if self._root:
            self._root.refresh()
        else:
            self.refresh_sublayouts()
            super().refresh(self._impl.viewport)

    def refresh_sublayouts(self):
        for child in self.children:
            child.refresh_sublayouts()

    def focus(self):
        if self._impl is not None:
            self._impl.focus()
