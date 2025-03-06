from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    ContextManager,
    Literal,
    Protocol,
)

from travertino.colors import Color

import toga
from toga.colors import BLACK
from toga.constants import FillRule
from toga.fonts import (
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    Font,
)
from toga.handlers import wrapped_handler

from ..base import StyleT, Widget
from .context import ClosedPathContext, Context, FillContext, StrokeContext

if TYPE_CHECKING:
    from toga.images import ImageT


class OnTouchHandler(Protocol):
    def __call__(self, widget: Canvas, x: int, y: int, **kwargs: Any) -> object:
        """A handler that will be invoked when a :any:`Canvas` is touched with a finger
        or mouse.

        :param widget: The canvas that was touched.
        :param x: X coordinate, relative to the left edge of the canvas.
        :param y: Y coordinate, relative to the top edge of the canvas.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class OnResizeHandler(Protocol):
    def __call__(
        self, widget: Canvas, width: int, height: int, **kwargs: Any
    ) -> object:
        """A handler that will be invoked when a :any:`Canvas` is resized.

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

        Inherits from :class:`toga.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param on_resize: Initial :any:`on_resize` handler.
        :param on_press: Initial :any:`on_press` handler.
        :param on_activate: Initial :any:`on_activate` handler.
        :param on_release: Initial :any:`on_release` handler.
        :param on_drag: Initial :any:`on_drag` handler.
        :param on_alt_press: Initial :any:`on_alt_press` handler.
        :param on_alt_release: Initial :any:`on_alt_release` handler.
        :param on_alt_drag: Initial :any:`on_alt_drag` handler.
        :param kwargs: Initial style properties.
        """
        self._context = Context(canvas=self)

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
    def context(self) -> Context:
        """The root context for the canvas."""
        return self._context

    def redraw(self) -> None:
        """Redraw the Canvas.

        The Canvas will be automatically redrawn after adding or removing a drawing
        object, or when the Canvas resizes. However, when you modify the properties of a
        drawing object, you must call ``redraw`` manually.
        """
        self._impl.redraw()

    def Context(self) -> ContextManager[Context]:
        """Construct and yield a new sub-:class:`~toga.widgets.canvas.Context` within
        the root context of this Canvas.

        :yields: The new :class:`~toga.widgets.canvas.Context` object.
        """
        return self.context.Context()

    def ClosedPath(
        self,
        x: float | None = None,
        y: float | None = None,
    ) -> ContextManager[ClosedPathContext]:
        """Construct and yield a new :class:`~toga.widgets.canvas.ClosedPathContext`
        context in the root context of this canvas.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :yields: The new :class:`~toga.widgets.canvas.ClosedPathContext` context object.
        """
        return self.context.ClosedPath(x, y)

    def Fill(
        self,
        x: float | None = None,
        y: float | None = None,
        color: Color | str | None = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
    ) -> ContextManager[FillContext]:
        """Construct and yield a new :class:`~toga.widgets.canvas.FillContext` in the
        root context of this canvas.

        A drawing operator that fills the path constructed in the context according to
        the current fill rule.

        If both an x and y coordinate is provided, the drawing context will begin with
        a ``move_to`` operation in that context.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :param fill_rule: `nonzero` is the non-zero winding rule; `evenodd` is the
            even-odd winding rule.
        :param color: The fill color.
        :yields: The new :class:`~toga.widgets.canvas.FillContext` context object.
        """
        return self.context.Fill(x, y, color, fill_rule)

    def Stroke(
        self,
        x: float | None = None,
        y: float | None = None,
        color: Color | str | None = BLACK,
        line_width: float = 2.0,
        line_dash: list[float] | None = None,
    ) -> ContextManager[StrokeContext]:
        """Construct and yield a new :class:`~toga.widgets.canvas.StrokeContext` in the
        root context of this canvas.

        If both an x and y coordinate is provided, the drawing context will begin with
        a ``move_to`` operation in that context.

        :param x: The x coordinate of the path's starting point.
        :param y: The y coordinate of the path's starting point.
        :param color: The color for the stroke.
        :param line_width: The width of the stroke.
        :param line_dash: The dash pattern to follow when drawing the line. Default is a
            solid line.
        :yields: The new :class:`~toga.widgets.canvas.StrokeContext` context object.
        """
        return self.context.Stroke(x, y, color, line_width, line_dash)

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
        """Measure the size at which :meth:`~.Context.write_text` would
        render some text.

        :param text: The text to measure. Newlines will cause line breaks, but long
            lines will not be wrapped.
        :param font: The font in which to draw the text. The default is the system font.
        :param line_height: Height of the line box as a multiple of the font size
            when multiple lines are present.
        :returns: A tuple of ``(width, height)``.
        """
        if font is None:
            font = Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE)

        if line_height is None:
            line_height = 1

        return self._impl.measure_text(str(text), font._impl, line_height)

    def as_image(self, format: type[ImageT] = toga.Image) -> ImageT:
        """Render the canvas as an image.

        :param format: Format to provide. Defaults to :class:`~toga.images.Image`; also
            supports :any:`PIL.Image.Image` if Pillow is installed, as well as any image
            types defined by installed :doc:`image format plugins
            </reference/plugins/image_formats>`
        :returns: The canvas as an image of the specified type.
        """
        return toga.Image(self._impl.get_image_data()).as_format(format)
