from __future__ import annotations

import warnings
from itertools import chain
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Protocol,
)
from weakref import WeakSet

import toga
from toga.colors import BLACK, Color
from toga.fonts import (
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    Font,
)
from toga.handlers import wrapped_handler

from ..base import StyleT, Widget
from .drawingaction import (
    Restore,
    Save,
    SetFillStyle,
    SetLineDash,
    SetLineWidth,
    SetStrokeStyle,
)
from .state import BaseState, DrawingActionDispatch, State

if TYPE_CHECKING:
    from toga.images import ColorT, ImageT

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)


BLACK_COLOR = Color.parse(BLACK)


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


class drawing_context_property:
    def __init__(self, ActionClass, default):
        self.ActionClass = ActionClass
        self.default = default

    def __set_name__(self, canvas_class, name):
        self.name = name

    def __get__(self, canvas, canvas_class=None):
        # Run down the nested hierarchy, building a chain of active states.
        state = canvas.root_state
        states = [state]

        while (
            state.drawing_actions
            # If it'st the active state then no substate of it can be currently open.
            and state is not canvas._action_target
            and isinstance(state.drawing_actions[-1], BaseState)
        ):
            state = state.drawing_actions[-1]
            states.append(state)

        # Then, run backwards through all active states' drawing actions until we hit a
        # setting. Restores build up, and are undone by saves.
        restores = 0
        for action in chain.from_iterable(
            reversed(state.drawing_actions) for state in reversed(states)
        ):
            if isinstance(action, Restore):
                restores += 1
            elif isinstance(action, Save):
                restores -= 1
            elif restores <= 0 and isinstance(action, self.ActionClass):
                return getattr(action, self.name)

        # It's never been set.
        return self.default

    def __set__(self, canvas, value):
        if value is None:
            self._raise()
        canvas._add_to_target(self.ActionClass(value))

    def __delete__(self, canvas, canvas_class=None):
        self._raise()

    def _raise(self):
        raise NotImplementedError(
            "Drawing context attributes can't be deleted or set to None. To reset to "
            "a default or previous value, do so explicitly or reset to a previous "
            "context state."
        )


class Canvas(Widget, DrawingActionDispatch):
    _MIN_WIDTH = 0
    _MIN_HEIGHT = 0

    # 2026-02: Backwards compatibility for <= 0.5.3
    _instances: WeakSet = WeakSet()

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
        self._root_state = State()

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
        self._instances.add(self)

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
        return self._root_state

    ###########################################################################
    # State management & attributes
    ###########################################################################

    def save(self) -> Save:
        """Save the current state of the drawing context.

        :returns: The `Save`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction] for the operation.
        """
        save = Save()
        self._add_to_target(save)
        # No need to redraw, since this has no visual effect.
        return save

    def restore(self) -> Save:
        """Restore to the previous state of the drawing context.

        :returns: The `Restore`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction] for the operation.
        """
        restore = Restore()
        self._add_to_target(restore)
        # No need to redraw, since this has no visual effect.
        return restore

    fill_style: ColorT = drawing_context_property(SetFillStyle, BLACK_COLOR)
    """The current fill color."""
    stroke_style: ColorT = drawing_context_property(SetStrokeStyle, BLACK_COLOR)
    """The current stroke color."""
    line_width: float = drawing_context_property(SetLineWidth, 2.0)
    """The current width of the stroke."""
    line_dash: list[float] = drawing_context_property(SetLineDash, [])
    """The current dash pattern to follow when drawing the line, expressed as
    alternating lengths of dashes and spaces. The default is a solid line.
    """

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
        return self._root_state

    ######################################################################
    # End backwards compatibility
    ######################################################################

    @property
    def _action_target(self):
        """Return the currently active state."""
        return self.root_state._active_state

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
