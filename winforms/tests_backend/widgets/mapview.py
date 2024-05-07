import asyncio

import pytest
from Microsoft.Web.WebView2.WinForms import WebView2

from .base import SimpleProbe


def region_eq(r1, r2):
    return (
        pytest.approx(r1[0]["lat"]) == pytest.approx(r2[0]["lat"])
        and pytest.approx(r1[1]["lat"]) == pytest.approx(r2[1]["lat"])
        and pytest.approx(r1[0]["lng"]) == pytest.approx(r2[0]["lng"])
        and pytest.approx(r1[1]["lng"]) == pytest.approx(r2[1]["lng"])
    )


class MapViewProbe(SimpleProbe):
    native_class = WebView2

    async def _map_region(self):
        northeast = self.impl._invoke("map.getBounds().getNorthEast();")
        southwest = self.impl._invoke("map.getBounds().getSouthWest();")
        return northeast, southwest

    async def tile_longitude_span(self):
        northeast, southwest = await self._map_region()
        return 256 * (northeast["lng"] - southwest["lng"]) / self.width

    @property
    def pin_count(self):
        return int(self.impl._invoke("Object.keys(pins).length;"))

    async def select_pin(self, pin):
        pytest.skip("Winforms MapView doesn't support selecting pins")

    async def wait_for_map(self, message, max_delay=0.5):
        initial = await self._map_region()
        previous = initial
        panning = True

        # Iterate until 2 successive reads of the region, 0.2s apart, return the same
        # value; or we've been waiting max_delay seconds. If confirm_pan is True, also
        # confirm that the value has actually changed from the initial value.
        tick_count = 0
        delta = 0.2
        while panning and tick_count < (max_delay / delta):
            await asyncio.sleep(delta)
            current = await self._map_region()

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
