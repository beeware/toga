from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import InitVar, dataclass, fields, is_dataclass
from enum import Enum
from math import pi
from typing import TYPE_CHECKING, Any
from warnings import filterwarnings, warn

from toga.colors import Color
from toga.constants import Baseline, FillRule
from toga.fonts import (
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    Font,
)
from toga.images import Image

from .geometry import CornerRadiusT

if TYPE_CHECKING:
    from toga.colors import ColorT

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
    """A drawing operation in a [`State`][toga.widgets.canvas.State].

    Every state drawing method creates a `DrawingAction`, adds it to the state,
    and returns it. Each argument passed to the method becomes a property of the
    `DrawingAction`, which can be modified as shown in the [Usage][] section.

    `DrawingActions` can also be created manually, then added to a state using the
    [`append()`][toga.widgets.canvas.State.append] or
    [`insert()`][toga.widgets.canvas.State.append] methods. Their constructors take
    the same arguments as the corresponding [`State`][toga.widgets.canvas.State]
    method, and their classes have the same names, but capitalized:

    * [`toga.widgets.canvas.Arc`][toga.widgets.canvas.State.arc]
    * [`toga.widgets.canvas.BeginPath`][toga.widgets.canvas.State.begin_path]
    * [`toga.widgets.canvas.BezierCurveTo`][toga.widgets.canvas.State.bezier_curve_to]
    * [`toga.widgets.canvas.ClosePath`][toga.widgets.canvas.State.close_path]
    * [`toga.widgets.canvas.Ellipse`][toga.widgets.canvas.State.ellipse]
    * [`toga.widgets.canvas.Fill`][toga.widgets.canvas.State.fill]
    * [`toga.widgets.canvas.LineTo`][toga.widgets.canvas.State.line_to]
    * [`toga.widgets.canvas.MoveTo`][toga.widgets.canvas.State.move_to]
    * [`toga.widgets.canvas.QuadraticCurveTo`][toga.widgets.canvas.State.quadratic_curve_to]
    * [`toga.widgets.canvas.Rect`][toga.widgets.canvas.State.rect]
    * [`toga.widgets.canvas.ResetTransform`][toga.widgets.canvas.State.reset_transform]
    * [`toga.widgets.canvas.Rotate`][toga.widgets.canvas.State.rotate]
    * [`toga.widgets.canvas.Scale`][toga.widgets.canvas.State.scale]
    * [`toga.widgets.canvas.Stroke`][toga.widgets.canvas.State.stroke]
    * [`toga.widgets.canvas.Translate`][toga.widgets.canvas.State.translate]
    * [`toga.widgets.canvas.WriteText`][toga.widgets.canvas.State.write_text]
    """  # noqa: E501

    # Disable the line-too-long check as there is no way to properly render the list
    # above with any given list item on multiple lines; an undesired space is added if
    # the link content is split on two lines.

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


class color_property:
    def __get__(self, action, action_class=None):
        if action is None:
            return self

        return action._color

    def __set__(self, action, value):
        if value is self or value is None:
            # value is self when no argument is supplied in the dataclass constructor;
            # this is how we define a default value for the hidden attribute.
            value = None
        else:
            value = Color.parse(value)

        action._color = value


class BeginPath(DrawingAction):
    def _draw(self, context: Any) -> None:
        context.begin_path()


class ClosePath(DrawingAction):
    def _draw(self, context: Any) -> None:
        context.close_path()


@dataclass(repr=False)
class Fill(DrawingAction):
    color: ColorT | None = color_property()
    fill_rule: FillRule = FillRule.NONZERO

    def _draw(self, context: Any) -> None:
        context.save()
        if self.color is not None:
            context.set_fill_style(self.color)
        context.fill(self.fill_rule)
        context.restore()


@dataclass(repr=False)
class Stroke(DrawingAction):
    color: ColorT | None = color_property()
    line_width: float | None = None
    line_dash: list[float] | None = None

    def _draw(self, context: Any) -> None:
        context.save()
        if self.color is not None:
            context.set_stroke_style(self.color)
        if self.line_width is not None:
            context.set_line_width(self.line_width)
        if self.line_dash is not None:
            context.set_line_dash(self.line_dash)
        context.stroke()
        context.restore()


@dataclass(repr=False)
class MoveTo(DrawingAction):
    x: float
    y: float

    def _draw(self, context: Any) -> None:
        context.move_to(self.x, self.y)


@dataclass(repr=False)
class LineTo(DrawingAction):
    x: float
    y: float

    def _draw(self, context: Any) -> None:
        context.line_to(self.x, self.y)


@dataclass(repr=False)
class BezierCurveTo(DrawingAction):
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
    cpx: float
    cpy: float
    x: float
    y: float

    def _draw(self, context: Any) -> None:
        context.quadratic_curve_to(self.cpx, self.cpy, self.x, self.y)


@dataclass(repr=False)
class Arc(DrawingAction):
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
    x: float
    y: float
    width: float
    height: float

    def _draw(self, context: Any) -> None:
        context.rect(self.x, self.y, self.width, self.height)


@dataclass(repr=False)
class RoundRect(DrawingAction):
    x: float
    y: float
    width: float
    height: float
    radii: float | CornerRadiusT | Iterable[float | CornerRadiusT]

    def _draw(self, context: Any) -> None:
        context.round_rect(self.x, self.y, self.width, self.height, self.radii)


@dataclass(repr=False)
class WriteText(DrawingAction):
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


@dataclass(repr=False)
class DrawImage(DrawingAction):
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


@dataclass(repr=False)
class Rotate(DrawingAction):
    radians: float

    def _draw(self, context: Any) -> None:
        context.rotate(self.radians)


@dataclass(repr=False)
class Scale(DrawingAction):
    sx: float
    sy: float

    def _draw(self, context: Any) -> None:
        context.scale(self.sx, self.sy)


@dataclass(repr=False)
class Translate(DrawingAction):
    tx: float
    ty: float

    def _draw(self, context: Any) -> None:
        context.translate(self.tx, self.ty)


class ResetTransform(DrawingAction):
    def _draw(self, context: Any) -> None:
        context.reset_transform()
