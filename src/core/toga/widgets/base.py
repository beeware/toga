
from builtins import id as identifier

from travertino.node import Node

from toga.style import Pack, TogaApplicator
from toga.platform import get_platform_factory


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

        self._id = id if id else identifier(self)
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
        """Add a node as a child of this one.
        Args:
            child: A node to add as a child to this node.

        Raises:
            ValueError: If this node is a leaf, and cannot have children.
        """
        for child in children:
            super().add(child)

            child.app = self.app
            child.window = self.window

            if self._impl:
                self._impl.add_child(child._impl)

    @property
    def app(self):
        """The App to which this widget belongs.
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
        """The Window to which this widget belongs.
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
            super().refresh(self._impl.viewport)
            self.refresh_sublayouts()

    def refresh_sublayouts(self):
        if self._children is not None:
            for child in self._children:
                child.refresh_sublayouts()
