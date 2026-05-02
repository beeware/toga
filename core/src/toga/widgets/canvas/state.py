from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from collections.abc import Iterable
from contextlib import AbstractContextManager
from dataclasses import KW_ONLY, InitVar, dataclass
from math import pi
from typing import TYPE_CHECKING, Any

from toga.colors import Color
from toga.constants import Baseline, FillRule
from toga.fonts import Font
from toga.images import Image

from .drawingaction import (
    Arc,
    BeginPath,
    BezierCurveTo,
    DrawImage,
    DrawingAction,
    Ellipse,
    LineTo,
    MoveTo,
    QuadraticCurveTo,
    Rect,
    ResetTransform,
    Rotate,
    RoundRect,
    Scale,
    Translate,
    WriteText,
)
from .geometry import CornerRadiusT

if TYPE_CHECKING:
    from toga.colors import ColorT

    from .canvas import Canvas
    from .drawingaction import DrawingAction

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)

NOT_PROVIDED = object()


class DrawingActionDispatch(ABC):
    @property
    @abstractmethod
    def _action_target(self):
        """The state that should receive the drawing actions."""

    def _add_to_target(self, drawing_action: DrawingAction):
        if actions := self._action_target.drawing_actions:
            last = actions[-1]
            if isinstance(last, BaseState):
                # If the most recent drawing action is (potentially) a context manager,
                # disable it so it can't be entered later, out of order.
                last._can_be_entered = False

        actions.append(drawing_action)

    ###########################################################################
    # Path manipulation
    ###########################################################################

    def begin_path(self) -> BeginPath:
        """Start a new path.

        :returns: The `BeginPath`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction] for the operation.
        """
        begin_path = BeginPath()
        self._add_to_target(begin_path)
        self._redraw_with_warning_if_state()
        return begin_path

    def close_path(self) -> AbstractContextManager[ClosePath]:
        """Close the current path.

        This closes the current path as a simple drawing operation. It should be paired
        with a [`begin_path()`][toga.Canvas.begin_path] operation, or else used as a
        context manager. If used as a context manager, it begins a path when entering,
        and closes it upon exiting.

        :returns: The `ClosePath`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction] for the operation.
        """
        close_path = ClosePath()
        self._add_to_target(close_path)
        self._redraw_with_warning_if_state()
        return close_path

    def move_to(self, x: float, y: float) -> MoveTo:
        """Moves the current point without drawing.

        :param x: The x coordinate of the new current point.
        :param y: The y coordinate of the new current point.
        :returns: The `MoveTo` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        move_to = MoveTo(x, y)
        self._add_to_target(move_to)
        self._redraw_with_warning_if_state()
        return move_to

    def line_to(self, x: float, y: float) -> LineTo:
        """Draw a line segment ending at a point.

        :param x: The x coordinate for the end point of the line segment.
        :param y: The y coordinate for the end point of the line segment.
        :returns: The `LineTo` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        line_to = LineTo(x, y)
        self._add_to_target(line_to)
        self._redraw_with_warning_if_state()
        return line_to

    def bezier_curve_to(
        self,
        cp1x: float,
        cp1y: float,
        cp2x: float,
        cp2y: float,
        x: float,
        y: float,
    ) -> BezierCurveTo:
        """Draw a Bézier curve.

        A Bézier curve requires three points. The first two are control points; the
        third is the end point for the curve. The starting point is the last point in
        the current path, which can be changed using `move_to()` before creating the
        Bézier curve.

        :param cp1y: The y coordinate for the first control point of the Bézier curve.
        :param cp1x: The x coordinate for the first control point of the Bézier curve.
        :param cp2x: The x coordinate for the second control point of the Bézier curve.
        :param cp2y: The y coordinate for the second control point of the Bézier curve.
        :param x: The x coordinate for the end point.
        :param y: The y coordinate for the end point.
        :returns: The `BezierCurveTo`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction] for the operation.
        """
        bezier_curve_to = BezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)
        self._add_to_target(bezier_curve_to)
        self._redraw_with_warning_if_state()
        return bezier_curve_to

    def quadratic_curve_to(
        self,
        cpx: float,
        cpy: float,
        x: float,
        y: float,
    ) -> QuadraticCurveTo:
        """Draw a quadratic curve.

        A quadratic curve requires two points. The first point is a control point; the
        second is the end point. The starting point of the curve is the last point in
        the current path, which can be changed using `moveTo()` before creating the
        quadratic curve.

        :param cpx: The x axis of the coordinate for the control point of the quadratic
            curve.
        :param cpy: The y axis of the coordinate for the control point of the quadratic
            curve.
        :param x: The x axis of the coordinate for the end point.
        :param y: The y axis of the coordinate for the end point.
        :returns: The `QuadraticCurveTo`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction] for the operation.
        """
        quadratic_curve_to = QuadraticCurveTo(cpx, cpy, x, y)
        self._add_to_target(quadratic_curve_to)
        self._redraw_with_warning_if_state()
        return quadratic_curve_to

    def arc(
        self,
        x: float,
        y: float,
        radius: float,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        counterclockwise: bool | None = None,
        anticlockwise: bool | None = None,  # DEPRECATED
    ) -> Arc:
        """Draw a circular arc.

        A full circle will be drawn by default; an arc can be drawn by specifying a
        start and end angle.

        :param x: The X coordinate of the circle's center.
        :param y: The Y coordinate of the circle's center.
        :param startangle: The start angle in radians, measured clockwise from the
            positive X axis.
        :param endangle: The end angle in radians, measured clockwise from the positive
            X axis.
        :param counterclockwise: If true, the arc is swept counterclockwise. The default
            is clockwise.
        :param anticlockwise: **DEPRECATED** - Use `counterclockwise`.
        :returns: The `Arc` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        arc = Arc(x, y, radius, startangle, endangle, counterclockwise, anticlockwise)
        self._add_to_target(arc)
        self._redraw_with_warning_if_state()
        return arc

    def ellipse(
        self,
        x: float,
        y: float,
        radiusx: float,
        radiusy: float,
        rotation: float = 0.0,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        counterclockwise: bool | None = None,
        anticlockwise: bool | None = None,  # DEPRECATED
    ) -> Ellipse:
        """Draw an elliptical arc.

        A full ellipse will be drawn by default; an arc can be drawn by specifying a
        start and end angle.

        :param x: The X coordinate of the ellipse's center.
        :param y: The Y coordinate of the ellipse's center.
        :param radiusx: The ellipse's horizontal axis radius.
        :param radiusy: The ellipse's vertical axis radius.
        :param rotation: The ellipse's rotation in radians, measured clockwise around
            its center.
        :param startangle: The start angle in radians, measured clockwise from the
            positive X axis.
        :param endangle: The end angle in radians, measured clockwise from the positive
            X axis.
        :param counterclockwise: If true, the arc is swept counterclockwise. The default
            is clockwise.
        :param anticlockwise: **DEPRECATED** - Use `counterclockwise`.
        :returns: The `Ellipse` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        ellipse = Ellipse(
            x,
            y,
            radiusx,
            radiusy,
            rotation,
            startangle,
            endangle,
            counterclockwise,
            anticlockwise,
        )
        self._add_to_target(ellipse)
        self._redraw_with_warning_if_state()
        return ellipse

    def rect(self, x: float, y: float, width: float, height: float) -> Rect:
        """Draw a rectangle.

        :param x: The horizontal coordinate of the left of the rectangle.
        :param y: The vertical coordinate of the top of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :returns: The `Rect` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        rect = Rect(x, y, width, height)
        self._add_to_target(rect)
        self._redraw_with_warning_if_state()
        return rect

    def round_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        radii: float | CornerRadiusT | Iterable[float | CornerRadiusT],
    ) -> RoundRect:
        """Draw a rounded rectangle.

        Corner radii can be provided as:
        - a single numerical radius for both x and y radius for all corners
        - an object with attributes "x" and "y" for the x and y radius for all corners
        - a list of 1 to 4 of the above

        If the list has:
        - length 1, then the item gives the radius of all corners
        - length 2, then the upper left and lower right corners use the first radius,
          and upper right and lower left use the second radius
        - length 3, then the upper left corner uses the first radius, the upper right
          and lower left use the second radius, and the lower right corner uses the
          third radius
        - length 4, then the radii are given in order upper left, upper right, lower
          left, lower right

        If the radii are too large for the width or height, then they will be scaled.

        :param x: The horizontal coordinate of the left of the rounded rectangle.
        :param y: The vertical coordinate of the top of the rounded rectangle.
        :param width: The width of the rounded rectangle.
        :param height: The height of the roundedrectangle.
        :param radii: The corner radii of the rounded rectangle.
        :returns: The `RoundRect` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        round_rect = RoundRect(x, y, width, height, radii)
        self._add_to_target(round_rect)
        self._redraw_with_warning_if_state()
        return round_rect

    def fill(
        self,
        fill_rule: FillRule = FillRule.NONZERO,
        *,
        fill_style: ColorT | None | object = NOT_PROVIDED,
        color: ColorT | None | object = NOT_PROVIDED,
    ) -> AbstractContextManager[Fill]:
        """Fill the current path.

        The fill can use either the
        [Non-Zero](https://en.wikipedia.org/wiki/Nonzero-rule) or
        [Even-Odd](https://en.wikipedia.org/wiki/Even-odd_rule) winding
        rule for filling paths.

        If used as a context manager, this begins a new path, and moves to the specified
        (`x`, `y`) coordinates (if both are specified). When the context is exited, the
        path is filled.

        :param fill_rule: `nonzero` is the non-zero winding rule; `evenodd` is the
            even-odd winding rule.
        :param fill_style: The fill style. At present, only accepts colors; gradients
            and patterns are not supported.
        :param color: Alias for fill_style.
        :returns: The `Fill` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        :raises TypeError: If both `fill_style` and `color` are provided.
        """
        fill = Fill(fill_rule, fill_style=fill_style, color=color)
        self._add_to_target(fill)
        # Strictly speaking, this doesn't need a warning or redraw, since BaseState
        # overwrites this method with its own shimmed version. But we might as well be
        # as helpful as possible.
        self._redraw_with_warning_if_state()
        return fill

    def stroke(
        self,
        *,
        stroke_style: ColorT | None | object = NOT_PROVIDED,
        color: ColorT | None | object = NOT_PROVIDED,
        line_width: float | None = None,
        line_dash: list[float] | None = None,
    ) -> AbstractContextManager[Stroke]:
        """Draw the current path as a stroke.

        If used as a context manager, this begins a new path, and moves to the specified
        (`x`, `y`) coordinates (if both are specified). When the context is exited, the
        path is stroked.

        :param stroke_style: The stroke style. At present, only accepts colors;
            gradients and patterns are not supported.
        :param color: Alias for fill_style.
        :param line_width: The width of the stroke.
        :param line_dash: The dash pattern to follow when drawing the line, expressed as
            alternating lengths of dashes and spaces. The default is a solid line.
        :returns: The `Stroke` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        :raises TypeError: If both `stroke_style` and `color` are provided.
        """
        stroke = Stroke(
            stroke_style=stroke_style,
            color=color,
            line_width=line_width,
            line_dash=line_dash,
        )
        self._add_to_target(stroke)
        # Strictly speaking, this doesn't need a warning or redraw, since BaseState
        # overwrites this method with its own shimmed version. But we might as well be
        # as helpful as possible.
        self._redraw_with_warning_if_state()
        return stroke

    ###########################################################################
    # Text drawing
    ###########################################################################

    def write_text(
        self,
        text: str,
        x: float = 0.0,
        y: float = 0.0,
        font: Font | None = None,
        baseline: Baseline = Baseline.ALPHABETIC,
        line_height: float | None = None,
    ) -> WriteText:
        """Write text at a given position.

        Drawing text is effectively a series of path operations, so the text will have
        the current color and fill properties.

        :param text: The text to draw. Newlines will cause line breaks, but long lines
            will not be wrapped.
        :param x: The X coordinate of the text's left edge.
        :param y: The Y coordinate: its meaning depends on `baseline`.
        :param font: The font in which to draw the text. The default is the system font.
        :param baseline: Alignment of text relative to the Y coordinate.
        :param line_height: Height of the line box as a multiple of the font size
            when multiple lines are present.
        :returns: The `WriteText` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the operation.
        """
        write_text = WriteText(text, x, y, font, baseline, line_height)
        self._add_to_target(write_text)
        self._redraw_with_warning_if_state()
        return write_text

    ###########################################################################
    # Bitmap drawing
    ###########################################################################

    def draw_image(
        self,
        image: Image,
        x: float = 0.0,
        y: float = 0.0,
        width: float | None = None,
        height: float | None = None,
    ):
        """Draw a Toga Image.

        The x, y coordinates specify the location of the bottom-left corner
        of the image. If supplied, the width and height specify the size
        of the image when it is rendered; the image will be
        scaled to fit.

        Drawing of images is performed with the current transformation matrix
        applied, so the destination rectangle of the image will be rotated,
        scaled and translated by any transformations which are currently applied.

        :param image: a Toga Image
        :param x: The x-coordinate of the bottom-left corner of the image when
            it is drawn.
        :param y: The y-coordinate of the bottom-left corner of the image when
            it is drawn.
        :param width: The width of the destination rectangle where the image
            will be drawn. The image will be scaled to fit the width. If the
            width is omitted, the natural width of the image will be used and
            no scaling will be done.
        :param height: The height of the destination rectangle where the image
            will be drawn. The image will be scaled to fit the height. If the
            height is omitted, the natural height of the image will be used and
            no scaling will be done.
        """
        draw_image = DrawImage(image, x, y, width, height)
        self._add_to_target(draw_image)
        self._redraw_with_warning_if_state()
        return draw_image

    ###########################################################################
    # Transformations
    ###########################################################################
    def rotate(self, radians: float) -> Rotate:
        """Add a rotation.

        :param radians: The angle to rotate clockwise in radians.
        :returns: The `Rotate` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the transformation.
        """
        rotate = Rotate(radians)
        self._add_to_target(rotate)
        self._redraw_with_warning_if_state()
        return rotate

    def scale(self, sx: float, sy: float) -> Scale:
        """Add a scaling transformation.

        :param sx: Scale factor for the X dimension. A negative value flips the
            image horizontally.
        :param sy: Scale factor for the Y dimension. A negative value flips the
            image vertically.
        :returns: The `Scale` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the transformation.
        """
        scale = Scale(sx, sy)
        self._add_to_target(scale)
        self._redraw_with_warning_if_state()
        return scale

    def translate(self, tx: float, ty: float) -> Translate:
        """Add a translation.

        :param tx: Translation for the X dimension.
        :param ty: Translation for the Y dimension.
        :returns: The `Translate` [`DrawingAction`][toga.widgets.canvas.DrawingAction]
            for the transformation.
        """
        translate = Translate(tx, ty)
        self._add_to_target(translate)
        self._redraw_with_warning_if_state()
        return translate

    def reset_transform(self) -> ResetTransform:
        """Reset all transformations.

        :returns: A `ResetTransform`
            [`DrawingAction`][toga.widgets.canvas.DrawingAction].
        """
        reset_transform = ResetTransform()
        self._add_to_target(reset_transform)
        self._redraw_with_warning_if_state()
        return reset_transform

    ###########################################################################
    # Sub-states of this state
    ###########################################################################

    def state(self) -> AbstractContextManager[State]:
        """A context manager that saves the current state of the Canvas context, and
        restores it upon exiting.

        :return: Yields the new `State`
          [`DrawingAction`][toga.widgets.canvas.DrawingAction].
        """
        state = State()
        self._add_to_target(state)
        self._redraw_with_warning_if_state()
        return state

    ######################################################################
    # 2026-02: Backwards compatibility for <= 0.5.3
    ######################################################################

    def _warn_context_manager(self, old_name, new_name, coordinates, extra=""):
        msg = f"The {old_name}() drawing method has been renamed to {new_name}()"
        if coordinates:
            msg += (
                ", and no longer accepts x and y coordinates as parameters. Instead, "
                f"call move_to(x, y) after entering the {new_name} context."
            )
        if extra:
            msg = msg.removesuffix(".") + f". {extra}"
        warnings.warn(msg, DeprecationWarning, stacklevel=3)

    # Each of these CamelCase methods, when called on a state, added to that state.
    # However, when called on a Canvas, they added to that Canvas's root_state. So we
    # call the drawing method on the target, suppressing warnings in case that target
    # is a state.

    def Context(self) -> AbstractContextManager[State]:
        self._warn_context_manager("Context", "state", False)

        target = self if isinstance(self, BaseState) else self.root_state
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            return target.state()

    def ClosedPath(
        self,
        x: float | None = None,
        y: float | None = None,
    ) -> AbstractContextManager[ClosePath]:
        self._warn_context_manager(
            "ClosedPath",
            "close_path",
            x is not None or y is not None,
        )

        target = self if isinstance(self, BaseState) else self.root_state
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            close_path = target.close_path()
        if x is not None and y is not None:
            # 4-2026: Backwards compatibility for Toga <= 0.5.4 / Toga Chart <= 0.2.1
            # This is a weird one. The straightforward approach would be to simply add a
            # MoveTo to the close_path.drawing_actions. However, while ClosedPath was
            # documented as a context manager, TogaChart (up to 0.2.1) uses it as a
            # standalone command, without ever entering it. Used this way, it acts like
            # a move followed by close; it never *begins* a path, so it can close the
            # final leg on a path that's already been going.

            # Therefore, unless and until the ClosePath is in fact entered, it needs to
            # fulfill this edge case. We store x and y on it, and when it's drawn, if
            # it hasn't been used as a context manager, it moves to these coordinates
            # before calling context.close_path().
            close_path.x = x
            close_path.y = y

            # The target.close_path() method already called a redraw, but we need to
            # update it now that the ClosedPath knows about its coordinates.
            self._redraw_with_warning_if_state()

        return close_path

    def Fill(
        self,
        x: float | None = None,
        y: float | None = None,
        color: ColorT | None = None,
        fill_rule: FillRule = FillRule.NONZERO,
    ) -> AbstractContextManager[Fill]:
        self._warn_context_manager(
            "Fill",
            "fill",
            x is not None or y is not None,
            extra=(
                "Additionally, the Canvas.fill() method's color parameter can only be "
                "provided via keyword. fill_rule is the only argument it accepts "
                "positionally."
            ),
        )

        target = self if isinstance(self, BaseState) else self.root_state
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            # BaseState.fill still uses old signature too.
            fill = target.fill(color=color, fill_rule=fill_rule)
        if x is not None and y is not None:
            fill.drawing_actions.append(MoveTo(x, y))
        return fill

    def Stroke(
        self,
        x: float | None = None,
        y: float | None = None,
        color: ColorT | None = None,
        line_width: float | None = None,
        line_dash: list[float] | None = None,
    ) -> AbstractContextManager[Stroke]:
        self._warn_context_manager(
            "Stroke",
            "stroke",
            x is not None or y is not None,
            extra=(
                "Additionally, the Canvas.stroke() method's arguments can only be "
                "provided as keywords. It does not accept any positional arguments."
            ),
        )

        target = self if isinstance(self, BaseState) else self.root_state
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            # BaseState.fill still uses old signature too.
            stroke = target.stroke(
                color=color,
                line_width=line_width,
                line_dash=line_dash,
            )
        if x is not None and y is not None:
            stroke.drawing_actions.append(MoveTo(x, y))
        return stroke

    def _redraw_without_warning(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.redraw()

    def _redraw_with_warning_if_state(self):
        if isinstance(self, BaseState):
            # If a drawing method is called on a state, we need to warn about that, but
            # then silence the additional warning that we'll cause when we internally
            # call redraw().
            warnings.warn(
                (
                    "Calling drawing methods on a state is deprecated. To add actions "
                    "to the currently active state, call drawing methods on the canvas."
                ),
                DeprecationWarning,
                stacklevel=3,
            )
            self._redraw_without_warning()
        else:
            # On a canvas, proceed as usual.
            self.redraw()

    ######################################################################
    # End Backwards compatibility
    ######################################################################


class BaseState(DrawingAction, DrawingActionDispatch, ABC):
    """A base class for all drawing actions that can function as state-saving context
    managers.
    """

    drawing_actions: list[DrawingAction]
    """The list of all drawing actions contained by this state.

    If you add or remove drawing actions to this list, you'll need to call
    [`Canvas.redraw()`][toga.Canvas.redraw] for the changes to be rendered.
    """

    def __init__(self):
        self.drawing_actions = []
        self._can_be_entered = True

    @abstractmethod
    def _draw(self, context: Any) -> None: ...

    @property
    def _action_target(self):
        # State itself holds its drawing actions.
        return self

    @property
    def _active_state(self):
        """Return the currently active state, either this or a sub-state."""
        if self.drawing_actions:
            # If a sub-state is active, it must be the last action in the list;
            # subsequent actions would be added to that sub-state (or a sub-state of
            # it).
            last = self.drawing_actions[-1]
            if getattr(last, "_is_open", False):
                return last._active_state

        return self

    def __enter__(self):
        if not self._can_be_entered:
            raise RuntimeError(
                "A Canvas context manager can only be entered once, and only before "
                "any subsequent drawing actions are added."
            )

        self._is_open = True
        self._can_be_entered = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._is_open = False
        # Don't suppress any exceptions
        return False

    ##########################################################################
    # 2026-04: Backwards compatibility for <= 0.5.3
    ##########################################################################

    # These preserve the old signature, and warn about the new one.

    def fill(
        self,
        color: ColorT | None = None,
        fill_rule: FillRule = FillRule.NONZERO,
    ) -> AbstractContextManager[Fill]:
        fill = Fill(fill_rule=fill_rule, fill_style=color)
        self._add_to_target(fill)
        warnings.warn(
            (
                "Calling drawing methods on a state is deprecated. To add actions "
                "to the currently active state, call drawing methods on the canvas. "
                "Additionally, the Canvas.fill() method's color parameter can only be "
                "provided via keyword. fill_rule is the only argument it accepts "
                "positionally."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        self._redraw_without_warning()
        return fill

    def stroke(
        self,
        color: ColorT | None = None,
        line_width: float | None = None,
        line_dash: list[float] | None = None,
    ) -> AbstractContextManager[Stroke]:
        stroke = Stroke(stroke_style=color, line_width=line_width, line_dash=line_dash)
        self._add_to_target(stroke)
        warnings.warn(
            (
                "Calling drawing methods on a state is deprecated. To add actions "
                "to the currently active state, call drawing methods on the canvas. "
                "Additionally, the Canvas.stroke() method's arguments can only be "
                "provided as keywords. It does not accept any positional arguments."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        self._redraw_without_warning()
        return stroke

    ###########################################################################
    # 2026-02: Backwards compatibility for Toga <= 0.5.3
    ###########################################################################

    def __len__(self) -> int:
        self._warn_list_methods()
        return len(self.drawing_actions)

    def __getitem__(self, index: int) -> DrawingAction:
        self._warn_list_methods()
        return self.drawing_actions[index]

    def append(self, obj: DrawingAction) -> None:
        self._warn_list_methods()
        self.drawing_actions.append(obj)
        self._redraw_without_warning()

    def insert(self, index: int, obj: DrawingAction) -> None:
        self._warn_list_methods()
        self.drawing_actions.insert(index, obj)
        self._redraw_without_warning()

    def remove(self, obj: DrawingAction) -> None:
        self._warn_list_methods()
        self.drawing_actions.remove(obj)
        self._redraw_without_warning()

    def clear(self) -> None:
        self._warn_list_methods()
        self.drawing_actions.clear()
        self._redraw_without_warning()

    @property
    def canvas(self) -> Canvas:
        warnings.warn(
            "States no longer hold a reference to their canvas.",
            DeprecationWarning,
            stacklevel=2,
        )

        from .canvas import Canvas

        # Get the first that matches.
        for canvas in Canvas._instances:
            if self is canvas.root_state or self in canvas.root_state:
                return canvas

        return None

    def redraw(self) -> None:
        warnings.warn(
            (
                f"{type(self).__name__}.redraw() is deprecated. Call the canvas's "
                "redraw() method instead."
            ),
            DeprecationWarning,
            stacklevel=2,
        )

        from .canvas import Canvas

        # Redraw any canvases that contain self; could be multiple.
        for canvas in Canvas._instances:
            if self is canvas.root_state or self in canvas.root_state:
                canvas.redraw()

    def _warn_list_methods(self) -> None:
        warnings.warn(
            (
                "A state's list-like methods (append, insert, remove, and clear), as "
                "well as implementing len() and indexing, are deprecated. Manipulate "
                "its drawing_actions directly, and then call redraw() on the canvas."
            ),
            DeprecationWarning,
            stacklevel=3,
        )

    ######################################################################
    # End backwards compatibility
    ######################################################################


@dataclass(repr=False)
class State(BaseState):
    def __post_init__(self):
        super().__init__()

    def _draw(self, context: Any) -> None:
        context.save()
        for action in self.drawing_actions:
            action._draw(context)
        context.restore()


@dataclass(repr=False)
class ClosePath(BaseState):
    def __post_init__(self):
        super().__init__()

    # Backwards compatibility for Toga <= 0.5.4
    # See DrawingActionDispatch.ClosedPath for explanation
    def __enter__(self):
        super().__enter__()

        if hasattr(self, "x") and hasattr(self, "y"):
            self.drawing_actions.append(MoveTo(self.x, self.y))

        return self

    # End backwards compatibility

    def _draw(self, context: Any) -> None:
        if not (hasattr(self, "_is_open") or self.drawing_actions):
            # Wasn't used as a context manager, nor had drawing actions manually added

            # 4-2026: Backwards compatibility for Toga <= 0.5.4
            # See DrawingActionDispatch.ClosedPath for explanation
            if hasattr(self, "x") and hasattr(self, "y"):
                context.move_to(self.x, self.y)
            # End backwards compatibility

            context.close_path()
            return

        context.save()
        context.begin_path()

        for action in self.drawing_actions:
            action._draw(context)

        context.close_path()
        context.restore()


class color_property:
    def __get__(self, action, action_class=None):
        if action is None:
            # This is what's returned in the constructor, if nothing is provided.
            return NOT_PROVIDED

        return action._color

    def __set__(self, action, value):
        if value is not None and value is not NOT_PROVIDED:
            value = Color.parse(value)

        action._color = value


@dataclass(repr=False)
class Fill(BaseState):
    # This will need to change to a pair of positional arguments in order to accommodate
    # (path), (fill_rule), or (path, fill_rule) usage as in JavaScript.
    fill_rule: FillRule = FillRule.NONZERO
    _: KW_ONLY
    fill_style: ColorT | None | object = color_property()
    color: InitVar[ColorT | None | object] = color_property()

    def __post_init__(self, color):
        super().__init__()

        if self.fill_style is not NOT_PROVIDED and color is not NOT_PROVIDED:
            raise TypeError("Both fill_style and color provided")

        if self.fill_style is NOT_PROVIDED:
            self.fill_style = None if color is NOT_PROVIDED else color

    def _draw(self, context: Any) -> None:
        context.save()
        if self.fill_style is not None:
            context.set_fill_style(self.fill_style)

        if hasattr(self, "_is_open") or self.drawing_actions:
            # Was used as a context manager (or had drawing actions manually added)
            context.in_fill = True  # 4-2026: Backwards compatibility for Toga <= 0.5.3
            context.begin_path()

            for action in self.drawing_actions:
                action._draw(context)

            context.in_fill = False  # 4-2026: Backwards compatibility for Toga <= 0.5.3

        context.fill(self.fill_rule)
        context.restore()


@dataclass(repr=False)
class Stroke(BaseState):
    # Path parameter (positional/keyword) will go here.
    _: KW_ONLY
    stroke_style: ColorT | None | object = color_property()
    color: InitVar[ColorT | None | object] = color_property()
    line_width: float | None = None
    line_dash: list[float] | None = None

    def __post_init__(self, color):
        super().__init__()

        if self.stroke_style is not NOT_PROVIDED and color is not NOT_PROVIDED:
            raise TypeError("Both stroke_style and color provided")

        if self.stroke_style is NOT_PROVIDED:
            self.stroke_style = None if color is NOT_PROVIDED else color

    def _draw(self, context: Any) -> None:
        context.save()
        if self.stroke_style is not None:
            context.set_stroke_style(self.stroke_style)
        if self.line_width is not None:
            context.set_line_width(self.line_width)
        if self.line_dash is not None:
            context.set_line_dash(self.line_dash)

        if hasattr(self, "_is_open") or self.drawing_actions:
            # Was used as a context manager (or had drawing actions manually added)
            context.in_stroke = True  # Backwards compatibility for Toga <= 0.5.3
            context.begin_path()

            for action in self.drawing_actions:
                action._draw(context)

            context.in_stroke = False  # Backwards compatibility for Toga <= 0.5.3

        context.stroke()
        context.restore()
