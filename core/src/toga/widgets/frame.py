from __future__ import annotations

from typing import Any, Literal

from .base import StyleT, Widget


class Frame(Widget):
    _USE_DEBUG_BACKGROUND = True

    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        content: Widget | None = None,
        title: str | None = None,
        **kwargs,
    ):
        """Create a new Frame container.

        A Frame is a container that visually groups its content using the
        platform's native grouping idiom (e.g. ``NSBox`` on macOS, ``GtkFrame``
        on GTK, a ``GroupBox`` on Windows, a ``MaterialCardView`` on Android). The
        exact appearance is determined by the platform style guide; it is not
        configurable.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param content: The content to display inside the frame.
        :param title: The title to display on the frame, or ``None`` for an
            untitled frame.
        :param kwargs: Initial style properties.
        """
        # Prime the attributes that the property setters / refresh path read,
        # before _create() (invoked by super().__init__) can run.
        self._content: Widget | None = None

        super().__init__(id, style, **kwargs)

        # The impl now exists, so the content/title can be assigned.
        self.title = title
        self.content = content

    def _create(self) -> Any:
        return self.factory.Frame(interface=self)

    @Widget.app.setter
    def app(self, app) -> None:
        # Invoke the superclass property setter
        Widget.app.fset(self, app)

        # The content isn't in self.children, so assign the app to it manually.
        if self._content:
            self._content.app = app

    @Widget.window.setter
    def window(self, window) -> None:
        # Invoke the superclass property setter
        Widget.window.fset(self, window)

        # The content isn't in self.children, so assign the window to it manually.
        if self._content:
            self._content.window = window

    @property
    def enabled(self) -> Literal[True]:
        """Is the widget currently enabled? i.e., can the user interact with the widget?

        Frame widgets cannot be disabled; this property will always return True; any
        attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: object) -> None:
        pass

    def focus(self) -> None:
        """No-op; Frame cannot accept input focus."""
        pass

    @property
    def content(self) -> Widget | None:
        """The content widget displayed inside the frame."""
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
    def title(self) -> str:
        """The title displayed on the frame (an empty string if untitled)."""
        return self._impl.get_title()

    @title.setter
    def title(self, value: object) -> None:
        self._impl.set_title("" if value is None else str(value))
        self.refresh()
