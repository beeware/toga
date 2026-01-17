from __future__ import annotations

from abc import ABC, abstractmethod
from math import pi
from typing import TYPE_CHECKING, Any
from warnings import filterwarnings, warn

from toga.colors import BLACK, Color
from toga.constants import Baseline, FillRule
from toga.fonts import (
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    Font,
)
from toga.images import Image

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


class DrawingObject(ABC):
    """A drawing operation in a [`Context`][toga.widgets.canvas.Context].

    Every context drawing method creates a `DrawingObject`, adds it to the context,
    and returns it. Each argument passed to the method becomes a property of the
    `DrawingObject`, which can be modified as shown in the [Usage][] section.

    `DrawingObjects` can also be created manually, then added to a context using the
    [`append()`][toga.widgets.canvas.Context.append] or
    [`insert()`][toga.widgets.canvas.Context.append] methods. Their constructors take
    the same arguments as the corresponding [`Context`][toga.widgets.canvas.Context]
    method, and their classes have the same names, but capitalized:

    * [`toga.widgets.canvas.Arc`][toga.widgets.canvas.Context.arc]
    * [`toga.widgets.canvas.BeginPath`][toga.widgets.canvas.Context.begin_path]
    * [`toga.widgets.canvas.BezierCurveTo`][toga.widgets.canvas.Context.bezier_curve_to]
    * [`toga.widgets.canvas.ClosePath`][toga.widgets.canvas.Context.close_path]
    * [`toga.widgets.canvas.Ellipse`][toga.widgets.canvas.Context.ellipse]
    * [`toga.widgets.canvas.Fill`][toga.widgets.canvas.Context.fill]
    * [`toga.widgets.canvas.LineTo`][toga.widgets.canvas.Context.line_to]
    * [`toga.widgets.canvas.MoveTo`][toga.widgets.canvas.Context.move_to]
    * [`toga.widgets.canvas.QuadraticCurveTo`][toga.widgets.canvas.Context.quadratic_curve_to]
    * [`toga.widgets.canvas.Rect`][toga.widgets.canvas.Context.rect]
    * [`toga.widgets.canvas.ResetTransform`][toga.widgets.canvas.Context.reset_transform]
    * [`toga.widgets.canvas.Rotate`][toga.widgets.canvas.Context.rotate]
    * [`toga.widgets.canvas.Scale`][toga.widgets.canvas.Context.scale]
    * [`toga.widgets.canvas.Stroke`][toga.widgets.canvas.Context.stroke]
    * [`toga.widgets.canvas.Translate`][toga.widgets.canvas.Context.translate]
    * [`toga.widgets.canvas.WriteText`][toga.widgets.canvas.Context.write_text]
    """  # noqa: E501

    # Disable the line-too-long check as there is no way to properly render the list
    # above with any given list item on multiple lines; an undesired space is added if
    # the link content is split on two lines.

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def _draw(self, context: Any) -> None: ...


class BeginPath(DrawingObject):
    def _draw(self, context: Any) -> None:
        context.begin_path()


class ClosePath(DrawingObject):
    def _draw(self, context: Any) -> None:
        context.close_path()


class Fill(DrawingObject):
    def __init__(
        self,
        color: ColorT = BLACK,
        fill_rule: FillRule = FillRule.NONZERO,
    ):
        super().__init__()
        self.color = color
        self.fill_rule = fill_rule

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(color={self.color!r}, "
            f"fill_rule={self.fill_rule})"
        )

    def _draw(self, context: Any) -> None:
        context.save()
        if self.color is not None:
            context.set_fill_style(self.color)
        context.fill(self.fill_rule)
        context.restore()

    @property
    def fill_rule(self) -> FillRule:
        return self._fill_rule

    @fill_rule.setter
    def fill_rule(self, fill_rule: FillRule) -> None:
        self._fill_rule = fill_rule

    @property
    def color(self) -> Color | None:
        return self._color

    @color.setter
    def color(self, value: ColorT | None) -> None:
        if value is None:
            self._color = None
        else:
            self._color = Color.parse(value)


class Stroke(DrawingObject):
    def __init__(
        self,
        color: ColorT | None = None,
        line_width: float | None = None,
        line_dash: list[float] | None = None,
    ):
        super().__init__()
        self.color = color
        self.line_width = line_width
        self.line_dash = line_dash

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(color={self.color!r}, "
            f"line_width={self.line_width}, line_dash={self.line_dash!r})"
        )

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

    @property
    def color(self) -> Color | None:
        return self._color

    @color.setter
    def color(self, value: ColorT | None) -> None:
        if value is None:
            self._color = None
        else:
            self._color = Color.parse(value)

    @property
    def line_width(self) -> float | None:
        return self._line_width

    @line_width.setter
    def line_width(self, value: float | None) -> None:
        self._line_width = None if value is None else float(value)

    @property
    def line_dash(self) -> list[float] | None:
        return self._line_dash

    @line_dash.setter
    def line_dash(self, value: list[float] | None) -> None:
        self._line_dash = value


class MoveTo(DrawingObject):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, context: Any) -> None:
        context.move_to(self.x, self.y)


class LineTo(DrawingObject):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, context: Any) -> None:
        context.line_to(self.x, self.y)


class BezierCurveTo(DrawingObject):
    def __init__(
        self, cp1x: float, cp1y: float, cp2x: float, cp2y: float, x: float, y: float
    ):
        self.cp1x = cp1x
        self.cp1y = cp1y
        self.cp2x = cp2x
        self.cp2y = cp2y
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(cp1x={self.cp1x}, cp1y={self.cp1y}, "
            f"cp2x={self.cp2x}, cp2y={self.cp2y}, "
            f"x={self.x}, y={self.y})"
        )

    def _draw(self, context: Any) -> None:
        context.bezier_curve_to(
            self.cp1x, self.cp1y, self.cp2x, self.cp2y, self.x, self.y
        )


class QuadraticCurveTo(DrawingObject):
    def __init__(self, cpx: float, cpy: float, x: float, y: float):
        self.cpx = cpx
        self.cpy = cpy
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(cpx={self.cpx}, cpy={self.cpy}, x={self.x}, y={self.y})"
        )

    def _draw(self, context: Any) -> None:
        context.quadratic_curve_to(self.cpx, self.cpy, self.x, self.y)


class Arc(DrawingObject):
    def __init__(
        self,
        x: float,
        y: float,
        radius: float,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        counterclockwise: bool | None = None,
        anticlockwise: bool | None = None,  # DEPRECATED
    ):
        ######################################################################
        # 03-2025: Backwards compatibility for Toga <= 0.5.1
        ######################################################################

        counterclockwise = _determine_counterclockwise(anticlockwise, counterclockwise)

        ######################################################################
        # End backwards compatibility
        ######################################################################

        self.x = x
        self.y = y
        self.radius = radius
        self.startangle = startangle
        self.endangle = endangle
        self.counterclockwise = counterclockwise

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"radius={self.radius}, startangle={self.startangle:.3f}, "
            f"endangle={self.endangle:.3f}, counterclockwise={self.counterclockwise})"
        )

    def _draw(self, context: Any) -> None:
        context.arc(
            self.x,
            self.y,
            self.radius,
            self.startangle,
            self.endangle,
            self.counterclockwise,
        )


class Ellipse(DrawingObject):
    def __init__(
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
    ):
        ######################################################################
        # 03-2025: Backwards compatibility for Toga <= 0.5.1
        ######################################################################

        counterclockwise = _determine_counterclockwise(anticlockwise, counterclockwise)

        ######################################################################
        # End backwards compatibility
        ######################################################################

        self.x = x
        self.y = y
        self.radiusx = radiusx
        self.radiusy = radiusy
        self.rotation = rotation
        self.startangle = startangle
        self.endangle = endangle
        self.counterclockwise = counterclockwise

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"radiusx={self.radiusx}, radiusy={self.radiusy}, "
            f"rotation={self.rotation:.3f}, startangle={self.startangle:.3f}, "
            f"endangle={self.endangle:.3f}, counterclockwise={self.counterclockwise})"
        )

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


class Rect(DrawingObject):
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"width={self.width}, height={self.height})"
        )

    def _draw(self, context: Any) -> None:
        context.rect(self.x, self.y, self.width, self.height)


class WriteText(DrawingObject):
    def __init__(
        self,
        text: str,
        x: float = 0.0,
        y: float = 0.0,
        font: Font | None = None,
        baseline: Baseline = Baseline.ALPHABETIC,
        line_height: float | None = None,
    ):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.baseline = baseline
        self.line_height = line_height

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(text={self.text!r}, x={self.x}, y={self.y}, "
            f"font={self.font!r}, baseline={self.baseline}, "
            f"line_height={self.line_height})"
        )

    def _draw(self, context: Any) -> None:
        context.write_text(
            str(self.text),
            self.x,
            self.y,
            self.font._impl,
            self.baseline,
            self.line_height,
        )

    @property
    def font(self) -> Font:
        return self._font

    @font.setter
    def font(self, value: Font | None) -> None:
        if value is None:
            self._font = Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE)
        else:
            self._font = value


class DrawImage(DrawingObject):
    def __init__(
        self,
        image: Image,
        x: float = 0.0,
        y: float = 0.0,
        width: float | None = None,
        height: float | None = None,
    ):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(image={self.image!r}, x={self.x}, y={self.y}, "
            f"width={self.width!r}, height={self.height})"
        )

    def _draw(self, context: Any) -> None:
        context.draw_image(
            self.image,
            self.x,
            self.y,
            self.width if self.width is not None else self.image.width,
            self.height if self.height is not None else self.image.height,
        )

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float | None):
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float | None):
        self._height = value


class Rotate(DrawingObject):
    def __init__(self, radians: float):
        self.radians = radians

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(radians={self.radians:.3f})"

    def _draw(self, context: Any) -> None:
        context.rotate(self.radians)


class Scale(DrawingObject):
    def __init__(self, sx: float, sy: float):
        self.sx = sx
        self.sy = sy

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sx={self.sx:.3f}, sy={self.sy:.3f})"

    def _draw(self, context: Any) -> None:
        context.scale(self.sx, self.sy)


class Translate(DrawingObject):
    def __init__(self, tx: float, ty: float):
        self.tx = tx
        self.ty = ty

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tx={self.tx}, ty={self.ty})"

    def _draw(self, context: Any) -> None:
        context.translate(self.tx, self.ty)


class ResetTransform(DrawingObject):
    def _draw(self, context: Any) -> None:
        context.reset_transform()
