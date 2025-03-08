from __future__ import annotations

from abc import ABC, abstractmethod
from math import pi
from typing import Any

from travertino.colors import Color

from toga.colors import BLACK, color as parse_color
from toga.constants import Baseline, FillRule
from toga.fonts import (
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    Font,
)


class DrawingObject(ABC):
    """A drawing operation in a :any:`Context`.

    Every context drawing method creates a ``DrawingObject``, adds it to the context,
    and returns it. Each argument passed to the method becomes a property of the
    ``DrawingObject``, which can be modified as shown in the `Usage`_ section.

    ``DrawingObjects`` can also be created manually, then added to a context using the
    :meth:`~Context.append` or :meth:`~Context.insert` methods. Their constructors take
    the same arguments as the corresponding :any:`Context` method, and their classes
    have the same names, but capitalized:

    * :meth:`toga.widgets.canvas.Arc <Context.arc>`
    * :meth:`toga.widgets.canvas.BeginPath <Context.begin_path>`
    * :meth:`toga.widgets.canvas.BezierCurveTo <Context.bezier_curve_to>`
    * :meth:`toga.widgets.canvas.ClosePath <Context.close_path>`
    * :meth:`toga.widgets.canvas.Ellipse <Context.ellipse>`
    * :meth:`toga.widgets.canvas.Fill <Context.fill>`
    * :meth:`toga.widgets.canvas.LineTo <Context.line_to>`
    * :meth:`toga.widgets.canvas.MoveTo <Context.move_to>`
    * :meth:`toga.widgets.canvas.QuadraticCurveTo <Context.quadratic_curve_to>`
    * :meth:`toga.widgets.canvas.Rect <Context.rect>`
    * :meth:`toga.widgets.canvas.ResetTransform <Context.reset_transform>`
    * :meth:`toga.widgets.canvas.Rotate <Context.rotate>`
    * :meth:`toga.widgets.canvas.Scale <Context.scale>`
    * :meth:`toga.widgets.canvas.Stroke <Context.stroke>`
    * :meth:`toga.widgets.canvas.Translate <Context.translate>`
    * :meth:`toga.widgets.canvas.WriteText <Context.write_text>`
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def _draw(self, impl: Any, **kwargs: Any) -> None: ...


class BeginPath(DrawingObject):
    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.begin_path(**kwargs)


class ClosePath(DrawingObject):
    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.close_path(**kwargs)


class Fill(DrawingObject):
    def __init__(
        self,
        color: str = BLACK,
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

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.fill(self.color, self.fill_rule, **kwargs)

    @property
    def fill_rule(self) -> FillRule:
        return self._fill_rule

    @fill_rule.setter
    def fill_rule(self, fill_rule: FillRule) -> None:
        self._fill_rule = fill_rule

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color | str | None) -> None:
        if value is None:
            self._color = parse_color(BLACK)
        else:
            self._color = parse_color(value)


class Stroke(DrawingObject):
    def __init__(
        self,
        color: Color | str | None = BLACK,
        line_width: float = 2.0,
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

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.stroke(self.color, self.line_width, self.line_dash, **kwargs)

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color | str | None) -> None:
        if value is None:
            self._color = parse_color(BLACK)
        else:
            self._color = parse_color(value)

    @property
    def line_width(self) -> float:
        return self._line_width

    @line_width.setter
    def line_width(self, value: float) -> None:
        self._line_width = float(value)

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

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.move_to(self.x, self.y, **kwargs)


class LineTo(DrawingObject):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.line_to(self.x, self.y, **kwargs)


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

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.bezier_curve_to(
            self.cp1x, self.cp1y, self.cp2x, self.cp2y, self.x, self.y, **kwargs
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

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.quadratic_curve_to(self.cpx, self.cpy, self.x, self.y, **kwargs)


class Arc(DrawingObject):
    def __init__(
        self,
        x: float,
        y: float,
        radius: float,
        startangle: float = 0.0,
        endangle: float = 2 * pi,
        anticlockwise: bool = False,
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"radius={self.radius}, startangle={self.startangle:.3f}, "
            f"endangle={self.endangle:.3f}, anticlockwise={self.anticlockwise})"
        )

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.arc(
            self.x,
            self.y,
            self.radius,
            self.startangle,
            self.endangle,
            self.anticlockwise,
            **kwargs,
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
        anticlockwise: bool = False,
    ):
        self.x = x
        self.y = y
        self.radiusx = radiusx
        self.radiusy = radiusy
        self.rotation = rotation
        self.startangle = startangle
        self.endangle = endangle
        self.anticlockwise = anticlockwise

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, "
            f"radiusx={self.radiusx}, radiusy={self.radiusy}, "
            f"rotation={self.rotation:.3f}, startangle={self.startangle:.3f}, "
            f"endangle={self.endangle:.3f}, anticlockwise={self.anticlockwise})"
        )

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.ellipse(
            self.x,
            self.y,
            self.radiusx,
            self.radiusy,
            self.rotation,
            self.startangle,
            self.endangle,
            self.anticlockwise,
            **kwargs,
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

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.rect(self.x, self.y, self.width, self.height, **kwargs)


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

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.write_text(
            str(self.text),
            self.x,
            self.y,
            self.font._impl,
            self.baseline,
            self.line_height,
            **kwargs,
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


class Rotate(DrawingObject):
    def __init__(self, radians: float):
        self.radians = radians

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(radians={self.radians:.3f})"

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.rotate(self.radians, **kwargs)


class Scale(DrawingObject):
    def __init__(self, sx: float, sy: float):
        self.sx = sx
        self.sy = sy

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sx={self.sx:.3f}, sy={self.sy:.3f})"

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.scale(self.sx, self.sy, **kwargs)


class Translate(DrawingObject):
    def __init__(self, tx: float, ty: float):
        self.tx = tx
        self.ty = ty

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tx={self.tx}, ty={self.ty})"

    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.translate(self.tx, self.ty, **kwargs)


class ResetTransform(DrawingObject):
    def _draw(self, impl: Any, **kwargs: Any) -> None:
        impl.reset_transform(**kwargs)
