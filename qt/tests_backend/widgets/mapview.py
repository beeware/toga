from PySide6.QtQuickWidgets import QQuickWidget
from pytest import approx

from toga.types import LatLng

from .base import SimpleProbe


def region_eq(r1, r2):
    return (
        approx(r1[0].latitude()) == approx(r2[0].latitude())
        and approx(r1[1].latitude()) == approx(r2[1].latitude())
        and approx(r1[0].longitude()) == approx(r2[0].longitude())
        and approx(r1[1].longitude()) == approx(r2[1].longitude())
    )


class MapViewProbe(SimpleProbe):
    native_class = QQuickWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = self.native.rootObject()

    @property
    def width(self):
        return self.native.width()

    @property
    def height(self):
        return self.native.height()

    async def _map_region(self):
        region_str = self.root.getMapRegionString()
        parts = [float(x) for x in region_str.split(",")]
        top_left = LatLng(parts[0], parts[3])
        bottom_right = LatLng(parts[2], parts[1])
        return top_left, bottom_right

    async def tile_longitude_span(self):
        northeast, southwest = await self._map_region()
        return 256 * (northeast.lng - southwest.lng) / self.width

    @property
    def pin_count(self):
        return self.root.numberPins()

    async def select_pin(self, pin):
        self.impl.bridge.pinClicked(pin.uid)

    async def wait_for_map(self, message, max_delay=0.5):
        await self.redraw(message)
