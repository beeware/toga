from __future__ import annotations

import sys
from typing import NamedTuple

if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias, TypeVar  # noqa:F401
else:
    from typing import TypeAlias, TypeVar  # noqa:F401


class LatLng(NamedTuple):
    """A geographic coordinate."""

    #: Latitude
    lat: float

    #: Longitude
    lng: float

    def __str__(self) -> str:
        return f"({self.lat:6f}, {self.lng:6f})"
