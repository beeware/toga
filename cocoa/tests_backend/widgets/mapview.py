from toga_cocoa.libs import MKMapView

from .base import SimpleProbe


class MapViewProbe(SimpleProbe):
    native_class = MKMapView

    async def latitude_span(self):
        return self.native.region.span.latitudeDelta

    @property
    def pin_count(self):
        return len(self.native.annotations)

    async def select_pin(self, pin):
        self.native.selectAnnotation(pin._native, animated=False)
        await self.redraw(f"{pin.title} pin has been selected")
