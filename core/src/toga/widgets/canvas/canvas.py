from __future__ import annotations

import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Protocol,
)
from weakref import ref

import toga
from toga.fonts import (
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    Font,
)
from toga.handlers import wrapped_handler

from ..base import StyleT, Widget
from .state import DrawingActionDispatch, State

if TYPE_CHECKING:
    from toga.images import ImageT

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)


class OnTouchHandler(Protocol):
    def __call__(self, widget: Canvas, x: int, y: int, **kwargs: Any) -> None:
        """A handler that will be invoked when a [`Canvas`][toga.Canvas] is
        touched with a finger or mouse.

        :param widget: The canvas that was touched.
        :param x: X coordinate, relative to the left edge of the canvas.
        :param y: Y coordinate, relative to the top edge of the canvas.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class OnResizeHandler(Protocol):
    def __call__(self, widget: Canvas, width: int, height: int, **kwargs: Any) -> None:
        """A handler that will be invoked when a [`Canvas`][toga.Canvas] is resized.

        :param widget: The canvas that was resized.
        :param width: The new width.
        :param height: The new height.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class Canvas(Widget, DrawingActionDispatch):
    _MIN_WIDTH = 0
    _MIN_HEIGHT = 0

    # 2026-02: Backwards compatibility for <= 0.5.3
    _instances: list[ref] = []

    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        on_resize: OnResizeHandler | None = None,
        on_press: OnTouchHandler | None = None,
        on_activate: OnTouchHandler | None = None,
        on_release: OnTouchHandler | None = None,
        on_drag: OnTouchHandler | None = None,
        on_alt_press: OnTouchHandler | None = None,
        on_alt_release: OnTouchHandler | None = None,
        on_alt_drag: OnTouchHandler | None = None,
        **kwargs,
    ):
        """Create a new Canvas widget.

        Inherits from [`toga.Widget`][].

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param on_resize: Initial [`on_resize`][toga.Canvas.on_resize] handler.
        :param on_press: Initial [`on_press`][toga.Canvas.on_press] handler.
        :param on_activate: Initial [`on_activate`][toga.Canvas.on_activate] handler.
        :param on_release: Initial [`on_release`][toga.Canvas.on_release] handler.
        :param on_drag: Initial [`on_drag`][toga.Canvas.on_drag] handler.
        :param on_alt_press: Initial [`on_alt_press`][toga.Canvas.on_alt_press] handler.
        :param on_alt_release: Initial [`on_alt_release`][toga.Canvas.on_alt_release]
            handler.
        :param on_alt_drag: Initial [`on_alt_drag`][toga.Canvas.on_alt_drag] handler.
        :param kwargs: Initial style properties.
        """
        self._state = State()

        super().__init__(id, style, **kwargs)

        # Set all the properties
        self.on_resize = on_resize
        self.on_press = on_press
        self.on_activate = on_activate
        self.on_release = on_release
        self.on_drag = on_drag
        self.on_alt_press = on_alt_press
        self.on_alt_release = on_alt_release
        self.on_alt_drag = on_alt_drag

        # 2026-02: Backwards compatibility for <= 0.5.3
        self._instances.append(ref(self))

    def _create(self) -> Any:
        return self.factory.Canvas(interface=self)

    @property
    def enabled(self) -> Literal[True]:
        """Is the widget currently enabled? i.e., can the user interact with the widget?
        Canvas widgets cannot be disabled; this property will always return
        True; any attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: object) -> None:
        pass

    def focus(self) -> None:
        """No-op; Canvas cannot accept input focus."""
        pass

    @property
    def root_state(self) -> State:
        """The root state for the canvas."""
        return self._state

    ######################################################################
    # 2026-02: Backwards compatibility for <= 0.5.3
    ######################################################################

    @property
    def context(self) -> State:
        warnings.warn(
            "Canvas.context has been renamed to Canvas.root_state",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._state

    ######################################################################
    # End backwards compatibility
    ######################################################################

    @property
    def _action_target(self):
        """Return the currently active state."""
        state = self.root_state

        while state.drawing_actions:
            for action in reversed(state.drawing_actions):
                # Look through its drawing actions, from the bottom up.
                if getattr(action, "_is_open", False):
                    # If it's currently open as a context manager, assign it to state
                    # and break out of the for loop.
                    state = action
                    break
            # If none of the drawing actions were open, break out of the while loop.
            else:
                break

        return state

    def redraw(self) -> None:
        """Redraw the Canvas.

        The Canvas will be automatically redrawn after calling its drawing methods.
        However, when you directly add, remove, or modify a drawing action, you must
        call `redraw` manually.
        """
        self._impl.redraw()

    @property
    def on_resize(self) -> OnResizeHandler:
        """The handler to invoke when the canvas is resized."""
        return self._on_resize

    @on_resize.setter
    def on_resize(self, handler: OnResizeHandler) -> None:
        self._on_resize = wrapped_handler(self, handler)

    @property
    def on_press(self) -> OnTouchHandler:
        """The handler invoked when the canvas is pressed. When a mouse is being used,
        this press will be with the primary (usually the left) mouse button."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler: OnTouchHandler) -> None:
        self._on_press = wrapped_handler(self, handler)

    @property
    def on_activate(self) -> OnTouchHandler:
        """The handler invoked when the canvas is pressed in a way indicating the
        pressed object should be activated. When a mouse is in use, this will usually be
        a double click with the primary (usually the left) mouse button.

        This event is not supported on Android or iOS."""
        return self._on_activate

    @on_activate.setter
    def on_activate(self, handler: OnTouchHandler) -> None:
        self._on_activate = wrapped_handler(self, handler)

    @property
    def on_release(self) -> OnTouchHandler:
        """The handler invoked when a press on the canvas ends."""
        return self._on_release

    @on_release.setter
    def on_release(self, handler: OnTouchHandler) -> None:
        self._on_release = wrapped_handler(self, handler)

    @property
    def on_drag(self) -> OnTouchHandler:
        """The handler invoked when the location of a press changes."""
        return self._on_drag

    @on_drag.setter
    def on_drag(self, handler: OnTouchHandler) -> None:
        self._on_drag = wrapped_handler(self, handler)

    @property
    def on_alt_press(self) -> OnTouchHandler:
        """The handler to invoke when the canvas is pressed in an alternate
        manner. This will usually correspond to a secondary (usually the right) mouse
        button press.

        This event is not supported on Android or iOS.
        """
        return self._on_alt_press

    @on_alt_press.setter
    def on_alt_press(self, handler: OnTouchHandler) -> None:
        self._on_alt_press = wrapped_handler(self, handler)

    @property
    def on_alt_release(self) -> OnTouchHandler:
        """The handler to invoke when an alternate press is released.

        This event is not supported on Android or iOS.
        """
        return self._on_alt_release

    @on_alt_release.setter
    def on_alt_release(self, handler: OnTouchHandler) -> None:
        self._on_alt_release = wrapped_handler(self, handler)

    @property
    def on_alt_drag(self) -> OnTouchHandler:
        """The handler to invoke when the location of an alternate press changes.

        This event is not supported on Android or iOS.
        """
        return self._on_alt_drag

    @on_alt_drag.setter
    def on_alt_drag(self, handler: OnTouchHandler) -> None:
        self._on_alt_drag = wrapped_handler(self, handler)

    def measure_text(
        self,
        text: str,
        font: Font | None = None,
        line_height: float | None = None,
    ) -> tuple[float, float]:
        """Measure the size at which
        [`Canvas.write_text`][toga.Canvas.write_text]
        would render some text.

        :param text: The text to measure. Newlines will cause line breaks, but long
            lines will not be wrapped.
        :param font: The font in which to draw the text. The default is the system font.
        :param line_height: Height of the line box as a multiple of the font size
            when multiple lines are present.
        :returns: A tuple of `(width, height)`.
        """
        if font is None:
            font = Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE)

        return self._impl.measure_text(str(text), font._impl, line_height)

    def as_image(self, format: type[ImageT] = toga.Image) -> ImageT:
        """Render the canvas as an image.

        :param format: Format to provide. Defaults to [`Image`][toga.images.Image]; also
            supports [`PIL.Image.Image`][] if Pillow is installed, as well as any image
            types defined by installed [image format plugins][image-format-plugins].
        :returns: The canvas as an image of the specified type.
        """
        return toga.Image(self._impl.get_image_data()).as_format(format)
