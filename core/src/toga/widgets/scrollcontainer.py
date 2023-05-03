import warnings

from .base import Widget


class ScrollContainer(Widget):
    """Instantiate a new instance of the scrollable container widget.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object.
            If no style is provided then a new one will be created for the widget.
        horizontal (bool):  If True enable horizontal scroll bar.
        vertical (bool): If True enable vertical scroll bar.
        content (:class:`~toga.widgets.base.Widget`): The content of the scroll window.
    """

    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    def __init__(
        self,
        id=None,
        style=None,
        horizontal=True,
        vertical=True,
        on_scroll=None,
        content=None,
        factory=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style)

        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self._vertical = vertical
        self._horizontal = horizontal
        self._content = None

        # Create a platform specific implementation of a Scroll Container
        self._impl = self.factory.ScrollContainer(interface=self)

        # Set all attributes
        self.vertical = vertical
        self.horizontal = horizontal
        self.content = content
        self.on_scroll = on_scroll

    @Widget.app.setter
    def app(self, app):
        # Invoke the superclass property setter
        Widget.app.fset(self, app)

        # Also assign the app to the content in the container
        if self.content:
            self.content.app = app

    @Widget.window.setter
    def window(self, window):
        # Invoke the superclass property setter
        Widget.window.fset(self, window)

        # Also assign the window to the content in the container
        if self._content:
            self._content.window = window

    @property
    def content(self):
        """Content of the scroll container.

        Returns:
            The content of the widget (:class:`~toga.widgets.base.Widget`).
        """
        return self._content

    @content.setter
    def content(self, widget):
        if widget:
            widget.app = self.app
            widget.window = self.window

            self._content = widget

            self._impl.set_content(widget._impl)
            self.refresh()

            widget.refresh()

    def refresh_sublayouts(self):
        """Refresh the layout and appearance of this widget."""
        if self._content:
            self._content.refresh()

    @property
    def vertical(self):
        """Shows whether vertical scrolling is enabled.

        Returns:
            (bool) True if enabled, False if disabled.
        """
        return self._vertical

    @vertical.setter
    def vertical(self, value):
        self._vertical = value
        self._impl.set_vertical(value)

    @property
    def horizontal(self):
        """Shows whether horizontal scrolling is enabled.

        Returns:
            (bool) True if enabled, False if disabled.
        """
        return self._horizontal

    @horizontal.setter
    def horizontal(self, value):
        self._horizontal = value
        self._impl.set_horizontal(value)

    @property
    def on_scroll(self):
        return self._on_scroll

    @on_scroll.setter
    def on_scroll(self, on_scroll):
        self._on_scroll = on_scroll
        self._impl.set_on_scroll(on_scroll)

    @property
    def horizontal_position(self):
        return self._impl.get_horizontal_position()

    @horizontal_position.setter
    def horizontal_position(self, horizontal_position):
        if not self.horizontal:
            raise ValueError(
                "Cannot set horizontal position when horizontal is not set."
            )
        self._impl.set_horizontal_position(horizontal_position)

    @property
    def vertical_position(self):
        return self._impl.get_vertical_position()

    @vertical_position.setter
    def vertical_position(self, vertical_position):
        if not self.vertical:
            raise ValueError("Cannot set vertical position when vertical is not set.")
        self._impl.set_vertical_position(vertical_position)
