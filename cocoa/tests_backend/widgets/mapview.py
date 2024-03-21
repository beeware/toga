import asyncio
import re

import pytest

from toga_cocoa.libs import MKMapView

from .base import SimpleProbe


def region_eq(r1, r2):
    return (
        pytest.approx(r1.span.latitudeDelta) == pytest.approx(r2.span.latitudeDelta)
        and pytest.approx(r1.span.longitudeDelta)
        == pytest.approx(r2.span.longitudeDelta)
        and pytest.approx(r1.center.latitude) == pytest.approx(r2.center.latitude)
        and pytest.approx(r1.center.longitude) == pytest.approx(r2.center.longitude)
    )


class MapViewProbe(SimpleProbe):
    native_class = MKMapView

    async def tile_longitude_span(self):
        # Native structures aren't exposed to the user, but they have __repr__ and
        # __str__ methods for debugging purposes. Invoke those methods to ensure that
        # they produce output in roughly the right shape.

        # MKCoordinateRegion
        assert re.match(
            (
                r"<MKCoordinateRegion\(<CLLocationCoordinate2D\(-?\d+\.\d{4}, -?\d+\.\d{4}\)>, "
                r"span=<MKCoordinateSpan\(-?\d+\.\d{4}, -?\d+\.\d{4}\)>\)>"
            ),
            repr(self.native.region),
        )
        assert re.match(
            r"\(-?\d+\.\d{4}, -?\d+\.\d{4}\), span=\(-?\d+\.\d{4}, -?\d+\.\d{4}\)",
            str(self.native.region),
        )

        # CLLocationCoordinat2D
        assert re.match(
            r"<CLLocationCoordinate2D\(-?\d+\.\d{4}, -?\d+\.\d{4}\)>",
            repr(self.native.region.center),
        )
        assert re.match(
            r"\(-?\d+\.\d{4}, -?\d+\.\d{4}\)",
            str(self.native.region.center),
        )

        # MKCoordinateSpan
        assert re.match(
            r"<MKCoordinateSpan\(-?\d+\.\d{4}, -?\d+\.\d{4}\)>",
            repr(self.native.region.span),
        )
        assert re.match(
            r"\(\d+\.\d{4}, \d+\.\d{4}\)",
            str(self.native.region.span),
        )

        return 256 * self.native.region.span.longitudeDelta / self.width

    @property
    def pin_count(self):
        return len(self.native.annotations)

    async def select_pin(self, pin):
        self.native.selectAnnotation(pin._native, animated=False)
        await self.redraw(f"{pin.title} pin has been selected")

    async def wait_for_map(self, message, max_delay=0.5):
        initial = self.native.region
        previous = initial
        panning = True

        # Iterate until 2 successive reads of the region, 0.1s apart, return the same
        # value; or we've been waiting max_delay seconds. If confirm_pan is True, also confirm
        # that the value has actually changed from the initial value.
        tick_count = 0
        delta = 0.1
        while panning and tick_count < (max_delay / delta):
            await asyncio.sleep(delta)
            current = self.native.region

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
