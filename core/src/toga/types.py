from __future__ import annotations

from typing import NamedTuple


class LatLng(NamedTuple):
    """A geographic coordinate."""

    #: Latitude
    lat: float

    #: Longitude
    lng: float

    def __str__(self):
        return f"({self.lat:6f}, {self.lng:6f})"
