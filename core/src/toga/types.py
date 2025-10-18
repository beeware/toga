from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

import toga

if TYPE_CHECKING:
    from typing import TypeAlias

    PositionT: TypeAlias = toga.Position | tuple[int, int]
    """
    A representation of a 2D position, in CSS pixels. This can be:

    * A tuple of 2 integers `(x,y)`; or
    * An instance of [toga.Position][].
    """
    SizeT: TypeAlias = toga.Size | tuple[int, int]
    """
    A representation of a 2D size, in CSS pixels. This can be:

    * A tuple of 2 integers `(x,y)`; or
    * An instance of [toga.Size][].
    """


class LatLng(NamedTuple):
    """A geographic coordinate."""

    lat: float
    """Latitude"""

    lng: float
    """Longitude"""

    def __str__(self) -> str:
        return f"({self.lat:6f}, {self.lng:6f})"


class Position(NamedTuple):
    """A 2D position."""

    x: int
    """X coordinate, in CSS pixels."""

    y: int
    """Y coordinate, in CSS pixels."""

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Position(self.x * other, self.y * other)


class Size(NamedTuple):
    """A 2D size."""

    width: int
    """Width, in CSS pixels."""

    height: int
    """Height, in CSS pixels."""

    def __str__(self) -> str:
        return f"({self.width} x {self.height})"

    def __mul__(self, other):
        return Size(self.width * other, self.height * other)
