from __future__ import annotations

import warnings
from contextlib import AbstractContextManager as ContextManager
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Protocol,
)

import toga
from toga.constants import FillRule
from toga.fonts import (
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    Font,
)
from toga.handlers import wrapped_handler

from ..base import StyleT, Widget
from .state import ClosedPathContext, FillContext, State, StrokeContext

if TYPE_CHECKING:
    from toga.colors import ColorT
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


class Canvas(Widget):
    _MIN_WIDTH = 0
    _MIN_HEIGHT = 0

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
        self._state = State(canvas=self)

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

    @property
    def context(self) -> State:
        warnings.warn(
            "Canvas.context has been renamed to Canvas.root_state",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._state

    def redraw(self) -> None:
        """Redraw the Canvas.

        The Canvas will be automatically redrawn after adding or removing a drawing
        object, or when the Canvas resizes. However, when you modify the properties of a
        drawing object, you must call `redraw` manually.
        """
        self._impl.redraw()

    def Context(self) -> ContextManager[State]:
        """Construct and yield a new sub-[`State`][toga.widgets.canvas.State] within
        the root state of this Canvas.

        :return: Yields the new [`State`][toga.widgets.canvas.State] object.
        """
        warnings.warn(
            "Canvas.Context() is deprecated. Use Canvas.root_state.state() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.root_state.state()

    def ClosedPath(
        self,
        x: float | None = None,
        y: float | None = None,
    ) -> ContextManager[ClosedPathContext]:
        """Construct and yield a new
        [`ClosedPathContext`][toga.widgets.canvas.ClosedPathContext]
        state in the root state of this canvas.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :return: Yields the new
            [`ClosedPathContext`][toga.widgets.canvas.ClosedPathContext] state object.
        """
        return self.root_state.ClosedPath(x, y)

    def Fill(
        self,
        x: float | None = None,
        y: float | None = None,
        color: ColorT | None = None,
        fill_rule: FillRule = FillRule.NONZERO,
    ) -> ContextManager[FillContext]:
        """Construct and yield a new [`FillContext`][toga.widgets.canvas.FillContext]
        in the root state of this canvas.

        A drawing operator that fills the path constructed in the state according to
        the current fill rule.

        If both an x and y coordinate is provided, the drawing state will begin with
        a `move_to` operation in that state.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :param fill_rule: `nonzero` is the non-zero winding rule; `evenodd` is the
            even-odd winding rule.
        :param color: The fill color.
        :return class: Yields the new [`FillContext`][toga.widgets.canvas.FillContext]
            state object.
        """
        return self.root_state.Fill(x, y, color, fill_rule)

    def Stroke(
        self,
        x: float | None = None,
        y: float | None = None,
        color: ColorT | None = None,
        line_width: float | None = None,
        line_dash: list[float] | None = None,
    ) -> ContextManager[StrokeContext]:
        """Construct and yield a new
        [`StrokeContext`][toga.widgets.canvas.StrokeContext] in the
        root state of this canvas.

        If both an x and y coordinate is provided, the drawing state will begin with
        a `move_to` operation in that state.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :param color: The color for the stroke.
        :param line_width: The width of the stroke.
        :param line_dash: The dash pattern to follow when drawing the line. Default is a
            solid line.
        :return: Yields the new
            [`StrokeContext`][toga.widgets.canvas.StrokeContext] state object.
        """
        return self.root_state.Stroke(x, y, color, line_width, line_dash)

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
        [`State.write_text`][toga.widgets.canvas.State.write_text]
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
