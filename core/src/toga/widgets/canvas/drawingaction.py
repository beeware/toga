from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import InitVar, dataclass, fields, is_dataclass
from enum import Enum
from math import pi
from typing import TYPE_CHECKING, Any
from warnings import filterwarnings, warn

from toga.colors import Color
from toga.constants import Baseline
from toga.fonts import (
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    Font,
)
from toga.images import Image

from .geometry import CornerRadiusT

if TYPE_CHECKING:
    from toga.colors import ColorT
    from toga.constants import Baseline

# Make sure deprecation warnings are shown by default
filterwarnings("default", category=DeprecationWarning)

######################################################################
# 03-2025: Backwards compatibility for Toga <= 0.5.1
######################################################################


def _determine_counterclockwise(anticlockwise, counterclockwise):
    num_supplied = sum(value is not None for value in [anticlockwise, counterclockwise])
    if num_supplied == 0:
        return False
    if num_supplied == 1:
        if anticlockwise is not None:
            warn(
                "Parameter 'anticlockwise' is deprecated. Use 'counterclockwise' "
                "instead.",
                DeprecationWarning,
                stacklevel=3,
            )
            return anticlockwise

        return counterclockwise

    raise TypeError("Received both 'anticlockwise' and 'counterclockwise' arguments")


######################################################################
# End backwards compatibility
######################################################################


class DrawingAction(ABC):
    """A [`Canvas`][toga.Canvas] drawing operation.

    Every canvas drawing method creates a `DrawingAction`, adds it to the currently
    active state, and returns it. Each argument passed to the method becomes a property
    of the `DrawingAction`, which can be modified as shown in
    [Modifying attributes of DrawingActions][].

    `DrawingActions` can also be
    [created manually][creating-and-adding-new-drawingactions]. Their constructors take
    the same arguments as the corresponding [`Canvas`][toga.Canvas] drawing method, and
    their classes have the same names, but capitalized.
    """

    def __repr__(self) -> str:
        if is_dataclass(self):
            str_fields = []
            for field in fields(self):
                match value := getattr(self, field.name):
                    case float():
                        str_value = f"{value:.3f}"
                    case Enum():
                        str_value = str(value)
                    case _:
                        str_value = repr(value)
                str_fields.append(f"{field.name}={str_value}")

            parenthetical = ", ".join(str_fields)

        else:
            parenthetical = ""

        return f"{type(self).__name__}({parenthetical})"

    @abstractmethod
    def _draw(self, context: Any) -> None:
        """Called by parent state to execute this drawing action."""

    def __contains__(self, other: DrawingAction):
        return hasattr(self, "drawing_actions") and any(
            action is other or other in action for action in self.drawing_actions
        )


NOT_PROVIDED = object()


class color_property:
    def __set_name__(self, action_class, name):
        self.name = name

    def __get__(self, action, action_class=None):
        print(f"Get called for {getattr(self, 'name', '<no name yet>')}")
        if action is None:
            print("\tAction is None; returning self")
            return self

        print(f"\tReturning _color: {action._color}")
        return action._color

    def __set__(self, action, value):
        print(f"Set called for {self.name} with value: {value}")
        if value not in {None, NOT_PROVIDED, self}:
            print("\tParsing...")
            value = Color.parse(value)
        else:
            print("\tNo parsing needed")

        print(f"Assigning value: {value}")
        action._color = value


###########################################################################
# State management
###########################################################################


class Save(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [save()][toga.Canvas.save] method.
    """

    def _draw(self, context: Any) -> None:
        context.save()


class Restore(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [restore()][toga.Canvas.restore] method.
    """

    def _draw(self, context: Any) -> None:
        context.restore()


###########################################################################
# Attribute setting
###########################################################################


@dataclass(repr=False)
class SetFillStyle(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing assigning to
    the [fill_style][toga.Canvas.fill_style] context attribute.
    """

    fill_style: ColorT = color_property()

    def _draw(self, context: Any) -> None:
        context.set_fill_style(self.fill_style)


@dataclass(repr=False)
class SetStrokeStyle(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing assigning to
    the [stroke_style][toga.Canvas.stroke_style] context attribute.
    """

    stroke_style: ColorT = color_property()

    def _draw(self, context: Any) -> None:
        context.set_stroke_style(self.stroke_style)


@dataclass(repr=False)
class SetLineDash(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing assigning to
    the [line_dash][toga.Canvas.line_dash] context attribute.
    """

    line_dash: list[float]

    def _draw(self, context: Any) -> None:
        context.set_line_dash(self.line_dash)


@dataclass(repr=False)
class SetLineWidth(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing assigning to
    the [line_width][toga.Canvas.line_width] context attribute.
    """

    line_width: float

    def _draw(self, context: Any) -> None:
        context.set_line_width(self.line_width)


###########################################################################
# Path manipulation
###########################################################################


class BeginPath(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [begin_path()][toga.Canvas.begin_path] method.
    """

    def _draw(self, context: Any) -> None:
        context.begin_path()


@dataclass(repr=False)
class MoveTo(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [move_to()][toga.Canvas.move_to] method.
    """

    x: float
    y: float

    def _draw(self, context: Any) -> None:
        context.move_to(self.x, self.y)


@dataclass(repr=False)
class LineTo(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [line_to()][toga.Canvas.line_to] method.
    """

    x: float
    y: float

    def _draw(self, context: Any) -> None:
        context.line_to(self.x, self.y)


@dataclass(repr=False)
class BezierCurveTo(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [bezier_curve_to()][toga.Canvas.bezier_curve_to] method.
    """

    cp1x: float
    cp1y: float
    cp2x: float
    cp2y: float
    x: float
    y: float

    def _draw(self, context: Any) -> None:
        context.bezier_curve_to(
            self.cp1x, self.cp1y, self.cp2x, self.cp2y, self.x, self.y
        )


@dataclass(repr=False)
class QuadraticCurveTo(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [quadratic_curve_to()][toga.Canvas.quadratic_curve_to] method.
    """

    cpx: float
    cpy: float
    x: float
    y: float

    def _draw(self, context: Any) -> None:
        context.quadratic_curve_to(self.cpx, self.cpy, self.x, self.y)


@dataclass(repr=False)
class Arc(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [arc()][toga.Canvas.arc] method.
    """

    x: float
    y: float
    radius: float
    startangle: float = 0.0
    endangle: float = 2 * pi
    counterclockwise: bool | None = None
    anticlockwise: InitVar[bool | None] = None  # DEPRECATED

    ######################################################################
    # 03-2025: Backwards compatibility for Toga <= 0.5.1
    ######################################################################

    def __post_init__(self, anticlockwise):
        self.counterclockwise = _determine_counterclockwise(
            anticlockwise, self.counterclockwise
        )

    ######################################################################
    # End backwards compatibility
    ######################################################################

    def _draw(self, context: Any) -> None:
        context.arc(
            self.x,
            self.y,
            self.radius,
            self.startangle,
            self.endangle,
            self.counterclockwise,
        )


@dataclass(repr=False)
class Ellipse(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [ellipse()][toga.Canvas.ellipse] method.
    """

    x: float
    y: float
    radiusx: float
    radiusy: float
    rotation: float = 0.0
    startangle: float = 0.0
    endangle: float = 2 * pi
    counterclockwise: bool | None = None
    anticlockwise: InitVar[bool | None] = None  # DEPRECATED

    ######################################################################
    # 03-2025: Backwards compatibility for Toga <= 0.5.1
    ######################################################################

    def __post_init__(self, anticlockwise):
        self.counterclockwise = _determine_counterclockwise(
            anticlockwise,
            self.counterclockwise,
        )

    ######################################################################
    # End backwards compatibility
    ######################################################################

    def _draw(self, context: Any) -> None:
        context.ellipse(
            self.x,
            self.y,
            self.radiusx,
            self.radiusy,
            self.rotation,
            self.startangle,
            self.endangle,
            self.counterclockwise,
        )


@dataclass(repr=False)
class Rect(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [rect()][toga.Canvas.rect] method.
    """

    x: float
    y: float
    width: float
    height: float

    def _draw(self, context: Any) -> None:
        context.rect(self.x, self.y, self.width, self.height)


@dataclass(repr=False)
class RoundRect(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [round_rect()][toga.Canvas.round_rect] method.
    """

    x: float
    y: float
    width: float
    height: float
    radii: float | CornerRadiusT | Iterable[float | CornerRadiusT]

    def _draw(self, context: Any) -> None:
        context.round_rect(self.x, self.y, self.width, self.height, self.radii)


###########################################################################
# Text drawing
###########################################################################


@dataclass(repr=False)
class WriteText(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [write_text()][toga.Canvas.write_text] method.
    """

    text: str
    x: float = 0.0
    y: float = 0.0
    font: Font | None = None
    baseline: Baseline = Baseline.ALPHABETIC
    line_height: float | None = None

    def _draw(self, context: Any) -> None:
        context.write_text(
            str(self.text),
            self.x,
            self.y,
            (
                self.font._impl
                if self.font is not None
                else Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE)._impl
            ),
            self.baseline,
            self.line_height,
        )


###########################################################################
# Bitmap drawing
###########################################################################


@dataclass(repr=False)
class DrawImage(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [draw_image()][toga.Canvas.draw_image] method.
    """

    image: Image
    x: float = 0.0
    y: float = 0.0
    width: float | None = None
    height: float | None = None

    def _draw(self, context: Any) -> None:
        context.draw_image(
            self.image,
            self.x,
            self.y,
            self.width if self.width is not None else self.image.width,
            self.height if self.height is not None else self.image.height,
        )


###########################################################################
# Transformations
###########################################################################


@dataclass(repr=False)
class Rotate(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [rotate()][toga.Canvas.rotate] method.
    """

    radians: float

    def _draw(self, context: Any) -> None:
        context.rotate(self.radians)


@dataclass(repr=False)
class Scale(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [scale()][toga.Canvas.scale] method.
    """

    sx: float
    sy: float

    def _draw(self, context: Any) -> None:
        context.scale(self.sx, self.sy)


@dataclass(repr=False)
class Translate(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [translate()][toga.Canvas.translate] method.
    """

    tx: float
    ty: float

    def _draw(self, context: Any) -> None:
        context.translate(self.tx, self.ty)


class ResetTransform(DrawingAction):
    """The [DrawingAction][toga.widgets.canvas.DrawingAction] representing the
    [reset_transform()][toga.Canvas.reset_transform] method.
    """

    def _draw(self, context: Any) -> None:
        context.reset_transform()
