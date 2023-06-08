from __future__ import annotations

from toga.handlers import wrapped_handler

from .base import Widget


class ScrollContainer(Widget):
    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    def __init__(
        self,
        id=None,
        style=None,
        horizontal: bool = True,
        vertical: bool = True,
        on_scroll: callable | None = None,
        content: Widget | None = None,
    ):
        """Create a new Scroll Container.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param horizontal: Should horizontal scrolling be permitted?
        :param vertical: Should horizontal scrolling be permitted?
        :param on_scroll: Initial :any:`on_scroll` handler.
        :param content: The content to display in the scroll window.
        """
        super().__init__(id=id, style=style)

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
        if self._content:
            self._content.app = app

    @Widget.window.setter
    def window(self, window):
        # Invoke the superclass property setter
        Widget.window.fset(self, window)

        # Also assign the window to the content in the container
        if self._content:
            self._content.window = window

    @property
    def content(self) -> Widget:
        """The root content widget displayed inside the scroll container."""
        return self._content

    @content.setter
    def content(self, widget):
        if self._content:
            self._content.app = None
            self._content.window = None

        if widget:
            widget.app = self.app
            widget.window = self.window

            self._content = widget
            self._impl.set_content(widget._impl)
        else:
            self._content = None
            self._impl.set_content(None)

        self.refresh()

    def refresh_sublayouts(self):
        """Refresh the layout and appearance of this widget."""
        if self._content:
            self._content.refresh()

    @property
    def vertical(self) -> bool:
        """Is vertical scrolling enabled?"""
        return self._impl.get_vertical()

    @vertical.setter
    def vertical(self, value):
        self._impl.set_vertical(bool(value))
        self.refresh_sublayouts()

    @property
    def horizontal(self) -> bool:
        """Is horizontal scrolling enabled?"""
        return self._impl.get_horizontal()

    @horizontal.setter
    def horizontal(self, value):
        self._impl.set_horizontal(bool(value))
        self.refresh_sublayouts()

    @property
    def on_scroll(self) -> callable:
        """Handler to invoke when the user moves a scroll bar."""
        return self._on_scroll

    @on_scroll.setter
    def on_scroll(self, on_scroll):
        self._on_scroll = wrapped_handler(self, on_scroll)

    @property
    def horizontal_position(self) -> float:
        """The current horizontal scroller position.

        Raises :any:`ValueError` if horizontal scrolling is not enabled.
        """
        if not self.horizontal:
            raise ValueError(
                "Cannot get horizontal position when horizontal is not set."
            )
        return self._impl.get_horizontal_position()

    @horizontal_position.setter
    def horizontal_position(self, horizontal_position):
        if not self.horizontal:
            raise ValueError(
                "Cannot set horizontal position when horizontal is not set."
            )
        self._impl.set_horizontal_position(float(horizontal_position))

    @property
    def vertical_position(self) -> float:
        """The current vertical scroller position.

        Raises :any:`ValueError` if vertical scrolling is not enabled.
        """
        if not self.vertical:
            raise ValueError("Cannot get vertical position when vertical is not set.")
        return self._impl.get_vertical_position()

    @vertical_position.setter
    def vertical_position(self, vertical_position):
        if not self.vertical:
            raise ValueError("Cannot set vertical position when vertical is not set.")
        self._impl.set_vertical_position(float(vertical_position))
