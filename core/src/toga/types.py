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


class LatLng(tuple):
    """A geographic coordinate, with optional altitude and accuracy attributes.

    A LatLng compares equal to a 2-tuple (lat, lng). The optional
    altitude, horizontal_accuracy, and vertical_accuracy attributes
    are not considered for equality or hashing.
    """

    altitude: float | None = None
    """Altitude in meters, or None if not available."""

    horizontal_accuracy: float | None = None
    """Horizontal accuracy in meters, or None if not available."""

    vertical_accuracy: float | None = None
    """Vertical accuracy in meters, or None if not available."""

    def __new__(
        cls,
        lat: float,
        lng: float,
        *,
        altitude: float | None = None,
        horizontal_accuracy: float | None = None,
        vertical_accuracy: float | None = None,
    ) -> LatLng:
        self = super().__new__(cls, (lat, lng))
        self.altitude = altitude
        self.horizontal_accuracy = horizontal_accuracy
        self.vertical_accuracy = vertical_accuracy
        return self

    @property
    def lat(self) -> float:
        """Latitude"""
        return self[0]

    @property
    def lng(self) -> float:
        """Longitude"""
        return self[1]

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
