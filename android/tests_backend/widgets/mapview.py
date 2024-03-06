import asyncio

import pytest
from org.osmdroid.views import MapView as OSMMapView

from .base import SimpleProbe


def region_eq(r1, r2):
    return (
        pytest.approx(r1[0].getLatitude()) == pytest.approx(r2[0].getLatitude())
        and pytest.approx(r1[0].getLongitude()) == pytest.approx(r2[0].getLongitude())
        and pytest.approx(r1[1]) == pytest.approx(r2[1])
        and pytest.approx(r1[2]) == pytest.approx(r2[2])
    )


class MapViewProbe(SimpleProbe):
    native_class = OSMMapView

    def _map_region(self):
        return (
            self.native.getMapCenter(),
            self.native.getLatitudeSpanDouble(),
            self.native.getLongitudeSpanDouble(),
        )

    async def tile_longitude_span(self):
        return 256 * self.native.getLongitudeSpanDouble() / self.width

    @property
    def pin_count(self):
        # OSMDroid doesn't differentiate between markers and other overlays.
        # There's always 1 overlay for the copyright notice.
        return self.native.getOverlays().size() - 1

    async def select_pin(self, pin):
        self.impl.marker_click_listener.onMarkerClick(pin._native, self.native)
        await self.redraw(f"{pin.title} pin has been selected")

    async def wait_for_map(self, message, max_delay=0.5):
        initial = self._map_region()
        previous = initial
        panning = True

        # Iterate until 2 successive reads of the region, 0.1s apart, return the same
        # value; or we've been waiting 2 seconds. If confirm_pan is True, also confirm
        # that the value has actually changed from the initial value.
        tick_count = 0
        while panning and tick_count < (max_delay / 0.1):
            await asyncio.sleep(0.1)
            current = self._map_region()
            # If the region isn't stable, we're still panning.
            panning = not region_eq(current, previous)

            # If the region is the same as the original region,
            # we're still waiting for panning to start. It's possible
            # panning has finished, but it's better to timeout on the
            # tick count to be sure
            if region_eq(current, initial):
                panning = True

            previous = current
            tick_count += 1

        await self.redraw(message)
