from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Protocol, SupportsInt

from toga.handlers import wrapped_handler
from toga.types import Position

from .base import StyleT, Widget

if TYPE_CHECKING:
    from toga.types import PositionT


class OnScrollHandler(Protocol):
    def __call__(self, widget: ScrollContainer, /, **kwargs: Any) -> object:
        """A handler to invoke when the container is scrolled.

        :param widget: The ScrollContainer that was scrolled.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class ScrollContainer(Widget):
    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        horizontal: bool = True,
        vertical: bool = True,
        on_scroll: OnScrollHandler | None = None,
        content: Widget | None = None,
    ):
        """Create a new Scroll Container.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param horizontal: Should horizontal scrolling be permitted?
        :param vertical: Should horizontal scrolling be permitted?
        :param on_scroll: Initial :any:`on_scroll` handler.
        :param content: The content to display in the scroll window.
        """
        super().__init__(id=id, style=style)

        self._content: Widget | None = None
        self.on_scroll = None

        # Create a platform specific implementation of a Scroll Container
        self._impl = self.factory.ScrollContainer(interface=self)

        # Set all attributes
        self.vertical = vertical
        self.horizontal = horizontal
        self.content = content
        self.on_scroll = on_scroll

    @Widget.app.setter
    def app(self, app) -> None:
        # Invoke the superclass property setter
        Widget.app.fset(self, app)

        # Also assign the app to the content in the container
        if self._content:
            self._content.app = app

    @Widget.window.setter
    def window(self, window) -> None:
        # Invoke the superclass property setter
        Widget.window.fset(self, window)

        # Also assign the window to the content in the container
        if self._content:
            self._content.window = window

    @property
    def enabled(self) -> Literal[True]:
        """Is the widget currently enabled? i.e., can the user interact with the widget?

        ScrollContainer widgets cannot be disabled; this property will always return
        True; any attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: object) -> None:
        pass

    def focus(self) -> None:
        """No-op; ScrollContainer cannot accept input focus."""
        pass

    @property
    def content(self) -> Widget | None:
        """The root content widget displayed inside the scroll container."""
        return self._content

    @content.setter
    def content(self, widget: Widget | None) -> None:
        if self._content:
            # Clear the window before the app so that registry entries can be cleared
            self._content.window = None
            self._content.app = None

        if widget:
            widget.app = self.app
            widget.window = self.window
            self._impl.set_content(widget._impl)
        else:
            self._impl.set_content(None)

        self._content = widget
        if widget:
            widget.refresh()

    @property
    def vertical(self) -> bool:
        """Is vertical scrolling enabled?"""
        return self._impl.get_vertical()

    @vertical.setter
    def vertical(self, value: object) -> None:
        self._impl.set_vertical(bool(value))
        if self._content:
            self._content.refresh()

    @property
    def horizontal(self) -> bool:
        """Is horizontal scrolling enabled?"""
        return self._impl.get_horizontal()

    @horizontal.setter
    def horizontal(self, value: object) -> None:
        self._impl.set_horizontal(bool(value))
        if self._content:
            self._content.refresh()

    @property
    def on_scroll(self) -> OnScrollHandler:
        """Handler to invoke when the user moves a scroll bar."""
        return self._on_scroll

    @on_scroll.setter
    def on_scroll(self, on_scroll: OnScrollHandler) -> None:
        self._on_scroll = wrapped_handler(self, on_scroll)

    @property
    def max_horizontal_position(self) -> int:
        """The maximum horizontal scroll position (read-only)."""
        if not self.horizontal:
            return 0
        else:
            return self._impl.get_max_horizontal_position()

    @property
    def horizontal_position(self) -> int:
        """The current horizontal scroll position.

        If the value provided is negative, or greater than the maximum horizontal
        position, the value will be clipped to the valid range.

        :returns: The current horizontal scroll position.
        :raises ValueError: If an attempt is made to change the horizontal position when
            horizontal scrolling is disabled.
        """
        return self._impl.get_horizontal_position()

    @horizontal_position.setter
    def horizontal_position(self, horizontal_position: SupportsInt) -> None:
        if not self.horizontal:
            raise ValueError(
                "Cannot set horizontal position when horizontal scrolling is not enabled."
            )

        self.position = (horizontal_position, self._impl.get_vertical_position())

    @property
    def max_vertical_position(self) -> int:
        """The maximum vertical scroll position (read-only)."""
        if not self.vertical:
            return 0
        else:
            return self._impl.get_max_vertical_position()

    @property
    def vertical_position(self) -> int:
        """The current vertical scroll position.

        If the value provided is negative, or greater than the maximum
        vertical position, the value will be clipped to the valid range.

        :returns: The current vertical scroll position.
        :raises ValueError: If an attempt is made to change the vertical position
            when vertical scrolling is disabled.
        """
        return self._impl.get_vertical_position()

    @vertical_position.setter
    def vertical_position(self, vertical_position: SupportsInt) -> None:
        if not self.vertical:
            raise ValueError(
                "Cannot set vertical position when vertical scrolling is not enabled."
            )

        self.position = (self._impl.get_horizontal_position(), vertical_position)

    # This combined property is necessary because on some platforms (e.g. iOS), setting
    # the horizontal and vertical position separately would cause the horizontal and
    # vertical movement to appear as two separate animations.
    @property
    def position(self) -> Position:
        """The current scroll position.

        If the value provided for either axis is negative, or greater than the maximum
        position in that axis, the value will be clipped to the valid range.

        If scrolling is disabled in either axis, the value provided for that axis will
        be ignored.
        """
        return Position(self.horizontal_position, self.vertical_position)

    @position.setter
    def position(self, position: PositionT):
        horizontal_position, vertical_position = map(int, position)
        if self.horizontal:
            if horizontal_position < 0:
                horizontal_position = 0
            else:
                max_value = self.max_horizontal_position
                if horizontal_position > max_value:
                    horizontal_position = max_value
        else:
            horizontal_position = self.horizontal_position

        if self.vertical:
            if vertical_position < 0:
                vertical_position = 0
            else:
                max_value = self.max_vertical_position
                if vertical_position > max_value:
                    vertical_position = max_value
        else:
            vertical_position = self.vertical_position

        self._impl.set_position(horizontal_position, vertical_position)
