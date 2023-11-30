from __future__ import annotations

import sys
from typing import NamedTuple

if sys.version_info < (3, 10):
    from typing_extensions import (  # noqa:F401
        TypeAlias as TypeAlias,
        TypeVar as TypeVar,
    )
else:
    from typing import TypeAlias as TypeAlias, TypeVar as TypeVar  # noqa:F401


class LatLng(NamedTuple):
    """A geographic coordinate."""

    #: Latitude
    lat: float

    #: Longitude
    lng: float

    def __str__(self) -> str:
        return f"({self.lat:6f}, {self.lng:6f})"
