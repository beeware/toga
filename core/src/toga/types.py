from __future__ import annotations

import sys
from typing import TYPE_CHECKING, NamedTuple

import toga

if TYPE_CHECKING:
    if sys.version_info < (3, 10):
        from typing_extensions import TypeAlias
    else:
        from typing import TypeAlias

    PositionT: TypeAlias = toga.Position | tuple[int, int]
    SizeT: TypeAlias = toga.Size | tuple[int, int]


class LatLng(NamedTuple):
    """A geographic coordinate."""

    #: Latitude
    lat: float

    #: Longitude
    lng: float

    def __str__(self) -> str:
        return f"({self.lat:6f}, {self.lng:6f})"


class Position(NamedTuple):
    """A 2D position."""

    #: X coordinate, in CSS pixels.
    x: int

    #: Y coordinate, in CSS pixels.
    y: int

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

    #: Width, in CSS pixels.
    width: int

    #: Height, in CSS pixels.
    height: int

    def __str__(self) -> str:
        return f"({self.width} x {self.height})"

    def __mul__(self, other):
        return Size(self.width * other, self.height * other)
