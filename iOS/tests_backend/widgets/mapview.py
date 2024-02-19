import re

from toga_iOS.libs import MKMapView

from .base import SimpleProbe


class MapViewProbe(SimpleProbe):
    native_class = MKMapView
    location_threshold = 0.0001

    async def latitude_span(self):
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

        return self.native.region.span.latitudeDelta

    @property
    def pin_count(self):
        return len(self.native.annotations)

    async def select_pin(self, pin):
        self.native.selectAnnotation(pin._native, animated=False)
        await self.redraw(f"{pin.title} pin has been selected")
